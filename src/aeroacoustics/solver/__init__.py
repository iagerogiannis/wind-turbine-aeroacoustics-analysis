import cmath
import csv
import os

from src.numerical_analysis import *
from ..lib import *
from .MBuilder import MBuilder
from .GridGenerator import GridGenerator
from .SourceSimulator import SourceSimulator


class Solver:
    def __init__(self, f, Lw, Temp, theta, u_star, z0, sigma_,
                 z_s, r_max, p_s, hr, results_dir, order=1, absorbing_layer=True):
        self.f = f
        self.Lw = Lw
        self.Temp = Temp
        self.theta = theta
        self.u_star = u_star
        self.z0 = z0
        self.sigma_ = sigma_
        self.z_s = z_s
        self.r_max = r_max
        self.p_s = p_s
        self.hr = hr
        self.order = order
        self.absorbing_layer = absorbing_layer
        self.a = self.calculate_a()
        self.c0 = self.calculate_c0()
        self.k0 = self.calculate_k0()
        self.Z = self.calculate_Z()

        self.results_dir = results_dir

        grid = GridGenerator(self.f, self.Temp, self.z_s, self.r_max, absorbing_layer=self.absorbing_layer)
        self.z = grid.z
        self.Dr = grid.Dr
        self.N = grid.N
        self.M = grid.M
        self.write_results_interval = grid.print_interval

        M_matrices = MBuilder(self.z, self.Dr, self.f, self.Temp, self.theta, self.u_star,
                              self.z0, self.sigma_, self.c0, self.k0, self.Z, self.a, self.order, self.absorbing_layer)
        self.M1, self.M2 = M_matrices.M1, M_matrices.M2

        source = SourceSimulator(self.z_s, self.Z, self.k0)
        self.psi = np.array([source.q_c(z_i) for z_i in self.z])

    def calculate_a(self):
        return atmospheric_attenuation_coefficient(self.f, self.Temp, self.p_s, self.hr)

    def calculate_c0(self):
        return nominal_speed_of_sound(self.Temp)

    def calculate_k0(self):
        return kappa(self.c0, self.f, atmospheric_absorption_term=self.a, absorbing_layer=False)

    def calculate_Z(self):
        return reduced_sound_impedance(self.f, self.sigma_)

    def R(self, i, j):
        return math.sqrt((self.z[i] - self.z_s) ** 2 + (j * self.Dr) ** 2)

    def p_free(self, i, j):
        R_ = self.R(i, j)
        return cmath.exp(1j * self.k0 * R_) / R_

    def pc_i(self, i, j):
        r = j * self.Dr
        return self.psi[i] * cmath.exp(1j * self.k0 * r) / math.sqrt(r)

    def DL_i(self, i, j):
        pc_abs = abs(self.pc_i(i, j))
        p_free_abs = abs(self.p_free(i, j))
        if pc_abs < p_free_abs:
            return 0.
        else:
            return 10. * math.log((pc_abs / p_free_abs) ** 2)

    def SPL_i(self, i, j):
        return sound_pressure_level(self.DL_i(i, j), self.Lw, self.R(i, j))

    def calculate_SPL(self, j):
        return np.array([self.SPL_i(i, j) for i in range(len(self.psi))])

    def M_times_psi(self, M):
        M_times_psi = np.empty(self.N, dtype='complex128')

        M_times_psi[0] = M[1][0] * self.psi[0] + M[2][0] * self.psi[1]
        M_times_psi[-1] = M[0][-1] * self.psi[-2] + M[1][-1] * self.psi[-1]

        for i in range(1, self.N - 1):
            M_times_psi[i] = M[0][i - 1] * self.psi[i - 1] + \
                             M[1][i] * self.psi[i] + \
                             M[2][i] * self.psi[i + 1]

        return M_times_psi

    def solve_field(self):
        def write_file(filename, data):
            with open(filename, 'w') as f:
                f.write(str(data))

        def write_csv_file(filename, data):
            with open(filename, 'w', newline='') as f:
                fwriter = csv.writer(f, delimiter=';')
                fwriter.writerow(data)

        print_results_period = 20

        if not os.path.exists('{}'.format(self.results_dir)):
            os.makedirs('{}'.format(self.results_dir))

        r = np.array([i * self.Dr for i in range(1, self.M + 2)])
        r_to_write = [r[i] for i in range(len(r)) if i % self.write_results_interval == 0]
        z_to_write = [self.z[i] for i in range(len(self.z)) if i % self.write_results_interval == 0]

        write_file('{}/Lw.dat'.format(self.results_dir), self.Lw)
        write_csv_file('{}/r.csv'.format(self.results_dir), r_to_write)
        write_csv_file('{}/z.csv'.format(self.results_dir), z_to_write)

        f = open('{}/SPL.csv'.format(self.results_dir), 'w', newline='')
        writer = csv.writer(f, delimiter=';')
        for j in range(1, self.M + 2):
            self.psi = tdma_solver(self.M2[0], self.M2[1], self.M2[2], self.M_times_psi(self.M1))
            if j % self.write_results_interval == 0:
                SPL = self.calculate_SPL(j)
                if self.write_results_interval > 1:
                    SPL_to_write = [SPL[i] for i in range(len(SPL)) if i % self.write_results_interval == 0]
                else:
                    SPL_to_write = SPL
                writer.writerow(SPL_to_write)
            if j % print_results_period == 0:
                print('', end='\r')
                print('Calculating... {}%'.format(round(100 * j // self.M), 1), end='', flush=True)

        f.close()
        print('', end='\r')
        print('Calculation completed')

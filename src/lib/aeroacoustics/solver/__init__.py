import cmath
import csv
import os

from src.lib.numerical_analysis import *
from ..lib import *
from .MBuilder import MBuilder
from .GridGenerator import GridGenerator
from .SourceSimulator import SourceSimulator


class Solver:
    def __init__(self, f, Lw, Temp, theta, u_star, z0, sigma_, z_s, r_max, p_s, hr, results_dir, order=1):
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
        self.a = self.calculate_a()
        self.c0 = self.calculate_c0()
        self.k0 = self.calculate_k0()
        self.Z = self.calculate_Z()

        self.results_dir = results_dir

        grid_generator = GridGenerator(self.f, self.Temp, self.z_s)
        self.z = grid_generator.z
        self.Dr = grid_generator.Dr
        self.N = grid_generator.N

        M_matrices = MBuilder(self.z, self.Dr, self.f, self.Temp, self.theta, self.u_star,
                              self.z0, self.sigma_, self.c0, self.k0, self.Z, self.a, self.order)
        self.M1, self.M2 = M_matrices.M1, M_matrices.M2

        source = SourceSimulator(self.z_s, self.Z, self.k0)
        self.psi = np.array([source.q_c(z_i) for z_i in self.z])

    def calculate_a(self):
        return atmospheric_attenuation_coefficient(self.f, self.Temp, self.p_s, self.hr)

    def calculate_c0(self):
        return nominal_speed_of_sound(self.Temp)

    def calculate_k0(self):
        return kappa(self.c0, self.f, atmospheric_absorption_term=self.a, check_absorbing_layer=False)

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
            with open(filename, 'w', newline='') as f:
                fwriter = csv.writer(f, delimiter=';')
                fwriter.writerow(data)

        print_results_period = 20

        M = int(math.ceil(self.r_max / self.Dr))

        if not os.path.exists('{}/f{}'.format(self.results_dir, self.f)):
            os.makedirs('{}/f{}'.format(self.results_dir, self.f))

        write_file('{}/f{}/z.csv'.format(self.results_dir, self.f), self.z)
        write_file('{}/f{}/r.csv'.format(self.results_dir, self.f), np.array([i * self.Dr for i in range(1, M + 2)]))

        f = open('{}/f{}/result.csv'.format(self.results_dir, self.f), 'w', newline='')
        writer = csv.writer(f, delimiter=';')
        for j in range(1, M + 2):
            self.psi = tdma_solver(self.M2[0], self.M2[1], self.M2[2], self.M_times_psi(self.M1))
            SPL = self.calculate_SPL(j)
            writer.writerow(SPL)
            if j % print_results_period == 0:
                print('', end='\r')
                print('Calculating... {}%'.format(round(100 * j // M), 1), end='', flush=True)

        f.close()
        print('', end='\r')
        print('Calculation completed for frequency: {}Hz'.format(self.f))

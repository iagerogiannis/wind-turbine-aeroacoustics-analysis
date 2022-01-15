import cmath
import csv
import os

from src.lib.numerical_analysis import *
from ..lib import *
from .MBuilder import MBuilder
from .GridGenerator import GridGenerator
from .SourceSimulator import SourceSimulator


class Solver:
    def __init__(self, f, Temp, theta, u_star, z0, sigma_, z_s, r_max, p_s, hr, order=1):
        self.f = f
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

        grid_generator = GridGenerator(self.f, self.Temp, self.z_s)
        self.z = grid_generator.z
        self.Dr = grid_generator.Dr
        self.N = grid_generator.N
        self.zt_index = grid_generator.zt_index

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

    def M_times_psi(self, M):
        M_times_psi = np.empty(self.N, dtype='complex128')

        M_times_psi[0] = M[1][0] * self.psi[0] + M[2][0] * self.psi[1]

        for i in range(1, self.N - 1):
            M_times_psi[i] = M[0][i - 1] * self.psi[i - 1] + \
                             M[1][i] * self.psi[i] + \
                             M[2][i] * self.psi[i + 1]

        M_times_psi[-1] = M[0][-1] * self.psi[-2] + M[1][-1] * self.psi[-1]

        return M_times_psi

    def solve_field(self):
        def write_file(filename, data):
            with open(filename, 'w', newline='') as f:
                fwriter = csv.writer(f, delimiter=';')
                fwriter.writerow(data)

        print_results_period = 20

        results_dir = '../results'

        print(100 * "*")
        print('Solving for frequency: {}Hz'.format(self.f))
        M = int(math.ceil(self.r_max / self.Dr))

        if not os.path.exists('{}/f{}'.format(results_dir, self.f)):
            os.makedirs('{}/f{}'.format(results_dir, self.f))

        write_file('{}/f{}/z.csv'.format(results_dir, self.f), self.z[:self.zt_index])
        write_file('{}/f{}/r.csv'.format(results_dir, self.f), np.array([i * self.Dr for i in range(1, M + 2)]))

        f = open('{}/f{}/result.csv'.format(results_dir, self.f), 'w', newline='')
        writer = csv.writer(f, delimiter=';')
        for i in range(1, M + 2):
            self.psi = tdma_solver(self.M1[0], self.M1[1], self.M1[2], self.M_times_psi(self.M2))
            # self.psi = tdma_solver(self.M2[0], self.M2[1], self.M2[2], self.M_times_psi(self.M1))
            SPL = self.calculate_SPL(i)
            writer.writerow(SPL)
            if i % print_results_period == 0:
                print('', end='\r')
                print('Calculating... {}%'.format(round(100 * i // M), 1), end='', flush=True)

        f.close()
        print('', end='\r')
        print('Calculation completed for frequency: {}Hz'.format(self.f))

    def pc_i(self, psi, j):
        r = j * self.Dr
        return psi * cmath.exp(1j * self.k0 * r) / math.sqrt(r)

    def calculate_pc(self, j):
        return np.array([self.pc_i(psi, j) for psi in self.psi[:self.zt_index]])

    def calculate_SPL(self, j):
        return np.array([sound_pressure_level(self.pc_i(psi, j)) for psi in self.psi[:self.zt_index]])

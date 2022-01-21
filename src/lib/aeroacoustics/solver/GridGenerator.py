import math

from ..lib import *


class GridGenerator:
    def __init__(self, f, Temp, z_s, r_max, total_nodes=4e6, default_Dz=True):
        self.f = f
        self.z_s = z_s
        self.r_max = r_max
        self.total_nodes = total_nodes
        self.default_Dz = default_Dz
        self.c0 = nominal_speed_of_sound(Temp)
        self.lambda_ = wave_length(self.f, self.c0)
        self.h_max = 4. * self.z_s + 50. * self.lambda_

        self.Dz = self.Dr = self.calculate_Dz()
        self.N = self.calculate_N(self.Dz)
        self.M = self.calculate_M(self.Dz)

        self.z_max = (self.N - 1) * self.Dz
        self.z = np.array([(i + 1) * self.Dz for i in range(self.N)])
        self.zt_index = np.argmax(self.z > 4 * z_s) - 1

        self.nodes = self.num_of_nodes(self.Dz)
        self.print_interval = self.calculate_nodes_printed_interval()

    def calculate_M(self, Dz):
        return int(math.ceil(self.r_max / Dz))

    def calculate_N(self, Dz):
        return int(math.ceil(self.h_max / Dz))

    def num_of_nodes(self, Dz):
        N = self.calculate_N(Dz)
        M = self.calculate_M(Dz)
        return M * N + M + N + 1

    def calculate_nodes_printed_interval(self):
        for i in range(2, 40):
            nodes = (self.M / i) * (self.N / i) + (self.M + self.N) / i + 1
            if nodes < self.total_nodes:
                return i - 1

    def calculate_printed_nodes(self):
        return (self.M / self.print_interval) * (self.N / self.print_interval) + \
               (self.M + self.N) / self.print_interval + 1

    def calculate_Dz(self):
        def quadratic_equation_solver(a, b, c):
            D = b ** 2 - 4 * a * c
            return (-b + math.sqrt(D)) / (2 * a), (-b - math.sqrt(D)) / (2 * a)
        total_nodes = self.total_nodes
        Dz = self.lambda_ / 10
        if self.default_Dz or self.num_of_nodes(Dz) > total_nodes:
            return Dz
        else:
            return quadratic_equation_solver(total_nodes - 1, -(self.h_max + self.r_max), - self.h_max * self.r_max)[0]


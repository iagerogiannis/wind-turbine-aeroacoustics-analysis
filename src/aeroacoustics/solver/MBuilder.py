from ..lib import *


class MBuilder:

    def __init__(self, z, Dr, f, Temp, theta, u_star, z0, sigma_, c0, k0, Z, a, order=1, absorbing_layer=True):
        # Initialization
        self.f = f
        self.Temp = Temp
        self.theta = theta
        self.u_star = u_star
        self.z0 = z0
        self.sigma_ = sigma_
        self.Z = Z
        self.c0 = c0
        self.k0 = k0
        self.a = a
        self.order = order
        self.absorbing_layer = absorbing_layer

        # Grid parameters
        self.z = z
        self.N = len(z)
        self.z_M = z[-1]
        self.z_t = self.z_M - 50. * wave_length(self.f, self.c0)
        self.Dz = self.Dr = Dr

        # Build M matrices
        self.M = self.initialize_T()
        g_ = alpha(self.k0) / self.Dz ** 2
        self.multiply_by_constant(g_)
        self.add_matrix_D()
        self.multiply_by_constant(self.Dr / 2.)
        self.M1, self.M2 = self.build_final_matrices()

    def betta(self, z_i):
        u_w = wind_velocity(z_i, self.u_star, self.z0)
        c = c_effective(u_w, self.theta, self.c0)
        k = kappa(c, self.f, z_i, self.z_t, self.z_M,
                  atmospheric_absorption_term=self.a, absorbing_layer=self.absorbing_layer)
        return betta(k, self.k0)

    def initialize_T(self):
        T_u = np.full(self.N - 1, 1., dtype='complex128')
        T_m = np.full(self.N, -2., dtype='complex128')
        T_d = np.full(self.N - 1, 1., dtype='complex128')

        sigma_1, sigma_2 = sigma(self.k0, self.Dz, self.Z, self.order)
        tau_1, tau_2 = tau(self.k0, self.Dz, self.order)

        T_m[0] += sigma_1
        T_u[0] += sigma_2

        T_m[-1] += tau_1
        T_d[-1] += tau_2

        return [T_d, T_m, T_u]

    def add_matrix_D(self):
        D = np.array([self.betta(z_i) for z_i in self.z])
        self.M[1] += D

    def multiply_by_constant(self, constant):
        self.M[0] *= constant
        self.M[1] *= constant
        self.M[2] *= constant

    def build_final_matrices(self):
        I = np.full(self.N, 1.)
        self.M[1] += I
        M2 = [-self.M[0], 2 * I - self.M[1], -self.M[2]]
        return [self.M, M2]

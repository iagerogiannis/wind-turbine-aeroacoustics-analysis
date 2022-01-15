import cmath


class SourceSimulator:
    def __init__(self, z_s, Z, k0):
        self.z_s = z_s
        self.Z = Z
        self.k0 = k0
        self.C = self.calculate_C()

    def calculate_C(self):
        return (self.Z - 1) / (self.Z + 1)

    def q_0(self, z):
        return cmath.sqrt(1j * self.k0) * cmath.exp(-.5 * self.k0 ** 2 * z ** 2)

    def q_c(self, z):
        return self.q_0(z - self.z_s) + self.C * self.q_0(z + self.z_s)

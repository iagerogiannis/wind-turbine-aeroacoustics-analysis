import numpy as np

from ..lib import *


class GridGenerator:
    def __init__(self, f, Temp, z_s):
        self.f = f
        self.c0 = nominal_speed_of_sound(Temp)
        self.lambda_ = wave_length(self.f, self.c0)
        self.Dz = self.Dr = self.lambda_ / 10.
        self.N = int(math.ceil((4. * z_s + 50. * self.lambda_) / self.Dz))
        self.z_max = (self.N - 1) * self.Dz
        self.z = np.array([(i + 1) * self.Dz for i in range(self.N)])
        self.zt_index = np.argmax(self.z > 4 * z_s) - 1

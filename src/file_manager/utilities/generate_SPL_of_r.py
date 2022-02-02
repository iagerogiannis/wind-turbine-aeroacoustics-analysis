import numpy as np


def generate_SPL_of_r(z, SPL, h):
    h_index = np.argmax(z > h)

    SPL_of_r = np.array([np.interp(h, [z[h_index - 1], z[h_index]], [SPL[h_index - 1][i], SPL[h_index][i]])
                         for i in range(SPL.shape[1])])

    return SPL_of_r

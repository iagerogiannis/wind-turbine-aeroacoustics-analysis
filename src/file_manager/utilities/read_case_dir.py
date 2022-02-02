import numpy as np


def read_case_dir(case_dir):
    r = np.genfromtxt('{}/r.csv'.format(case_dir), delimiter=';')[1:]
    z = np.genfromtxt('{}/z.csv'.format(case_dir), delimiter=';')
    SPL = np.genfromtxt('{}/SPL.csv'.format(case_dir), delimiter=';')[1:].transpose()

    if r.shape[0] != SPL.shape[1]:
        r = r[:-1]

    return r, z, SPL

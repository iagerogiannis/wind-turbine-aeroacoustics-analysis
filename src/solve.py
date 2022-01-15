import os
import shutil

from src.lib.aeroacoustics.lib import *
from src.lib.aeroacoustics.solver import Solver


def clear_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def print_title():
    print(50 * "#")
    print("#" + 48 * " " + "#")
    print("#    Aeroacoustics Analysis for Wind Turbine     #")
    print("#" + 48 * " " + "#")
    print(50 * "#")
    print()


def solve(f):
    z_s = 50.                                       # iyos plimnis
    r_max = 350.                                    # orizontia apostash apo a/g

    Temp = C_to_K(20.)                              # thermokrasia
    hr = .7                                         # sxetikh ygrasia
    ps = atm_to_pa(1.)                              # atmosfairikh piesh
    sigma_ = 3.e5                                   # antistash rohs toy edafoys
    z0 = .01                                        # traxythta edafous
    u_star = .4                                     # taxythta tribhs
    theta = 0

    # Fasma hxhtikhs isxyos
    # Lw = [85., 90., 95., 103., 110., 110., 105., 99.5, 97.5, 84.5]

    print_title()
    clear_folder('../results')
    for f_i in f:
        solver = Solver(f_i, Temp, theta, u_star, z0, sigma_, z_s, r_max, ps, hr, order=2)
        solver.solve_field()

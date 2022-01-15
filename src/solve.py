from lib.aeroacoustics import Solver
from lib.units import *

from lib.output import *
from lib.file_manager import *


def solve(f, results_dir, delete_old=True):
    z_s = 50.                                       # iyos plimnis
    r_max = 350.                                    # orizontia apostash apo a/g

    Temp = C_to_K(20.)                              # thermokrasia
    hr = .7                                         # sxetikh ygrasia
    ps = atm_to_pa(1.)                              # atmosfairikh piesh
    sigma_ = 3.e5                                   # antistash rohs toy edafoys
    z0 = .01                                        # traxythta edafous
    u_star = .4                                     # taxythta tribhs
    theta = 0

    if delete_old:
        clear_folder(results_dir)
    for f_i in f:
        solver = Solver(f_i, Temp, theta, u_star, z0, sigma_, z_s, r_max, ps, hr, results_dir, order=2)
        solver.solve_field()

    print_divider()

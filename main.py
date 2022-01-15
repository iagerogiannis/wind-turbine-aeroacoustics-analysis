from lib.aeroacoustics.lib import *
from lib.aeroacoustics.solver import Solver

z_s = 50.                                       # iyos plimnis
h2 = 14.                                        # iyos ston 4o orofo
r_max = 350.                                    # orizontia apostash apo a/g
d = math.sqrt((z_s - h2) ** 2 + r_max ** 2)     # apostash apo a/g

Temp = C_to_K(20.)                              # thermokrasia
hr = .7                                         # sxetikh ygrasia
ps = atm_to_pa(1.)                              # atmosfairikh piesh
# ps = 1.                                       # atmosfairikh piesh
sigma_ = 3.e5                                   # antistash rohs toy edafoys
z0 = .01                                        # traxythta edafous
K = .35                                         # stathera Karman
u_star = .4                                     # taxythta tribhs
theta = 0

# Fasma hxhtikhs isxyos
f = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.]
Lw = [85., 90., 95., 103., 110., 110., 105., 99.5, 97.5, 84.5]

# for f_i in f[:1]:
for f_i in [500.]:
    solver = Solver(f_i, Temp, theta, u_star, z0, sigma_, z_s, r_max, ps, hr, order=2)
    solver.solve_field()

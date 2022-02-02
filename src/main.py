import math

from src.aeroacoustics import Solver
from src.file_manager import *
from src.output.console import *
from src.output.plot import *
from src.units import *

results_dir = '../results_without_absorbing_layer'
totals_dir = '{}/total'.format(results_dir)

# iyos dekth
h = 14

# Dedomena
z_s = 50.  # iyos plimnis
r_max = 350.  # orizontia apostash apo a/g

Temp = C_to_K(20.)  # thermokrasia
hr = .7  # sxetikh ygrasia
ps = atm_to_pa(1.)  # atmosfairikh piesh
sigma_ = 3.e5  # antistash rohs toy edafoys
z0 = .01  # traxythta edafous
u_star = .4  # taxythta tribhs

f = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.]
Lw = [85., 90., 95., 103., 110., 110., 105., 99.5, 97.5, 84.5]

theta = [0., math.pi]

f_to_calculate = [500.]
f_to_plot = [250., 1000., 4000.]

order = 2
should_delete_old = False
absorbing_layer = False

print_title()

for i in range(len(f)):
    if f[i] in f_to_calculate:
        for theta_i in theta:
            full_results_dir = "{}/f{}/theta{}".format(results_dir, str(f[i]), int(math.degrees(theta_i)))
            if should_delete_old:
                clear_folder(full_results_dir)
            print('Frequency: {}Hz | Theta: {}deg'.format(f[i], int(math.degrees(theta_i))))
            solver = Solver(f[i], Lw[i], Temp, theta_i, u_star, z0, sigma_,
                            z_s, r_max, ps, hr, full_results_dir, order=order, absorbing_layer=absorbing_layer)
            solver.solve_field()
            plot_for_case(f[i], h, theta_i, full_results_dir)
            print_divider()

# data = read_and_generate_data(results_dir)
# write_total_data(results_dir, data)
# plot_spectrum(totals_dir)
# plot_SPL_of_r(totals_dir, data, f_to_plot)

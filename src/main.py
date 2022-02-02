from src.aeroacoustics import Solver
from src.file_manager import *
from src.output.console import *
from src.output.plot import *

from src.data import *
from src.config import *


print_title()

for i in range(len(f)):
    if f[i] in f_to_calculate:
        for theta_i in theta:
            full_results_dir = "{}/f{}/theta{}".format(results_dir, str(f[i]), int(math.degrees(theta_i)))
            if should_delete_old_results:
                clear_folder(full_results_dir)
            print('Frequency: {}Hz | Theta: {}deg'.format(f[i], int(math.degrees(theta_i))))
            # solver = Solver(f[i], Lw[i], Temp, theta_i, u_star, z0, sigma_,
            #                 z_s, r_max, ps, hr, full_results_dir, order=order, absorbing_layer=absorbing_layer)
            # solver.solve_field()
            plot_for_case(f[i], h, theta_i, full_results_dir)
            print_divider()

# data = read_and_generate_data(results_dir)
# write_total_data(results_dir, data)
# plot_spectrum(totals_dir)
# plot_SPL_of_r(totals_dir, data, f_to_plot)

import pandas as pd

from src.file_manager import read_case_dir, generate_SPL_of_r
from ..lib import plot_scatter, plot_contour
from ..config import configuration


def plot_for_case(frequency, h, theta, case_dir):
    print('Creating plots...', end='', flush=True)

    r, z, SPL = read_case_dir(case_dir)
    SPL_of_r = generate_SPL_of_r(z, SPL, h)

    pd.DataFrame({
        "r [m]": r,
        "SPL [dB]": SPL_of_r
    }).to_csv('{}/SPL_of_r.csv'.format(case_dir), sep=';', index=False, encoding='utf-8')

    plot_scatter([r, SPL_of_r],
                 title='SPL - r for frequency {}Hz and theta {}deg'.format(
                     str(frequency), str(int(theta))),
                 x_label='r [m]', y_label='SPL [dB]',
                 filename='{}/SPL_of_r.png'.format(case_dir))

    plot_contour(r, z, SPL, configuration["contour_levels"],
                 z_max_percentage=configuration["z_max_percentage"],
                 z_max_abs=configuration["z_max_abs"],
                 cmap=configuration["color_map"],
                 x_label='r [m]', y_label='z [m]', z_label='SPL [dB]',
                 title=configuration["title"].format(
                     str(frequency), str(int(theta))),
                 filename='{}/contour_with_layer.png'.format(case_dir))

    plot_contour(r, z, SPL, configuration["contour_levels"],
                 z_max_percentage=configuration["z_max_percentage"],
                 z_max_abs=configuration["z_max_abs"],
                 cmap=configuration["color_map"],
                 x_label='r [m]', y_label='z [m]', z_label='SPL [dB]', y_max=200.,
                 title=configuration["title"].format(
                     str(frequency), str(int(theta))),
                 filename='{}/contour.png'.format(case_dir))

    print('', end='\r')
    print('Plots created')

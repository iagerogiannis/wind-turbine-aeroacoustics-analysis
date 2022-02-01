from src.file_manager import read_case_dir, generate_SPL_of_r
from ..lib import plot_scatter, plot_contour


def plot_for_case(frequency, h, theta, case_dir):
    print('Creating plots...', end='', flush=True)

    r, z, SPL = read_case_dir(case_dir)
    SPL_of_r = generate_SPL_of_r(z, SPL, h)

    plot_scatter([r, SPL_of_r],
                 title='SPL - r for frequency {}Hz and theta {}deg'.format(
                     str(frequency), str(int(theta))),
                 x_label='r [m]', y_label='SPL [dB]',
                 filename='{}/SPL_of_r.png'.format(case_dir))

    plot_contour(r, z, SPL, 200, z_max_percentage=.7, cmap='Spectral_r',
                 x_label='r [m]', y_label='z [m]', z_label='SPL [dB]',
                 title='SPL contour for frequency {}Hz and theta {}deg'.format(
                     str(frequency), str(int(theta))),
                 filename='{}/contour_with_layer.png'.format(case_dir))

    plot_contour(r, z, SPL, 200, z_max_percentage=.7, y_max=200., cmap='Spectral_r',
                 x_label='r [m]', y_label='z [m]', z_label='SPL [dB]',
                 title='SPL contour for frequency {}Hz and theta {}deg'.format(
                     str(frequency), str(int(theta))),
                 filename='{}/contour.png'.format(case_dir))

    print('', end='\r')
    print('Plots created')

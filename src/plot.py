import numpy as np
from lib.output.plots import *


def plot(frequencies, Lw, h, results_dir):

    SPL_spectrum = []
    SPL_for_r = []

    for frequency in frequencies:
        print('Creating plots for frequency {}Hz...'.format(str(frequency)), end='', flush=True)

        r = np.genfromtxt('{}/f{}/r.csv'.format(results_dir, str(frequency)), delimiter=';')[1:]
        z = np.genfromtxt('{}/f{}/z.csv'.format(results_dir, str(frequency)), delimiter=';')
        SPL = np.genfromtxt('{}/f{}/SPL.csv'.format(results_dir, str(frequency)), delimiter=';')[1:].transpose()

        if r.shape[0] != SPL.shape[1]:
            r = r[:-1]

        h_index = np.argmax(z > h)

        SPL_according_to_r = np.array([np.interp(h, [z[h_index - 1], z[h_index]],
                                                 [SPL[h_index - 1][i], SPL[h_index][i]]) for i in range(SPL.shape[1])])

        SPL_spectrum.append(SPL_according_to_r[-1])

        SPL_for_r.append(r)
        SPL_for_r.append(SPL_according_to_r)

        plot_scatter([r, SPL_according_to_r], title='Sound Pressure Level [dB] for frequency {}Hz'.format(str(frequency)),
                     x_label='r [m]', y_label='SPL [dB]',
                     filename='{}/f{}/SPL_of_r.png'.format(results_dir, str(frequency)))

        plot_contour(r, z, SPL, 200, z_max_percentage=.7, y_max=200., cmap='Spectral_r', x_label='r [m]', y_label='z [m]',
                     title='Sound Pressure Level [dB] for frequency {}Hz'.format(str(frequency)),
                     filename='{}/f{}/contour.png'.format(results_dir, str(frequency)))

        print('', end='\r')
        print('Plots created for frequency: {}Hz'.format(str(frequency)))

    plot_scatter(SPL_for_r,
                 x_label='r [m]', y_label='SPL [dB]', legend=['f = {}Hz'.format(f) for f in frequencies],
                 title='Sound Pressure Level [dB] at height {}m'.format(h),
                 filename='{}/SPL.png'.format(results_dir))

    plot_scatter([frequencies, SPL_spectrum, frequencies, Lw[:len(SPL_spectrum)]],
                 x_label='Frequency [Hz]', y_label='SPL [dB]', legend=['Lp', 'Lw'],
                 title='Sound Pressure Level compared to Sound Power Level',
                 filename='{}/spectrum.png'.format(results_dir))

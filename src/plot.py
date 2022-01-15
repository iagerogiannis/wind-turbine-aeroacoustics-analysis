import os

import numpy as np
import matplotlib.pyplot as plt


def plot(frequencies, results_dir):
    def plot_contour(x, y, z, levels=20, color_bar=True, title=None, x_label=None,
                     y_label=None, cmap='Spectral', filename=None):
        fig, ax = plt.subplots(1, 1)
        cp = ax.contourf(x, y, z, levels, cmap=cmap)

        if color_bar:
            fig.colorbar(cp)
        if title:
            ax.set_title(title, fontname='Arial', fontsize=16, fontweight="bold")
        if x_label:
            ax.set_xlabel(x_label, fontname='Arial', fontsize=14)
        if y_label:
            ax.set_ylabel(y_label, fontname='Arial', fontsize=14)

        if filename:
            plt.savefig(filename)
        else:
            plt.show()

    if not os.path.exists('{}/plots'.format(results_dir)):
        os.makedirs('{}/plots'.format(results_dir))

    for frequency in frequencies:
        print('Creating plot for frequency {}Hz...'.format(str(frequency)), end='', flush=True)

        X = np.genfromtxt('{}/f{}/r.csv'.format(results_dir, str(frequency)), delimiter=';')[1:]
        Y = np.genfromtxt('{}/f{}/z.csv'.format(results_dir, str(frequency)), delimiter=';')
        Z = np.genfromtxt('{}/f{}/result.csv'.format(results_dir, str(frequency)), delimiter=';')[1:].transpose()
        plot_contour(X, Y, Z, 200, cmap='Spectral', x_label='r [m]', y_label='z [m]',
                     title='Sound Pressure Level [dB] for frequency {}Hz'.format(str(frequency)),
                     filename='{}/plots/f{}.png'.format(results_dir, str(frequency)))

        print('', end='\r')
        print('Plot created for frequency: {}Hz'.format(str(frequency)))

import os

import numpy as np
import matplotlib.pyplot as plt


def plot_contour(x, y, z, levels=20, color_bar=True, title=None, x_label=None, y_label=None, cmap='Spectral', filename=None):
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


# directories = next(os.walk('results'))[1]
# directories = ['f500.0', 'f1000.0']
num_of_freqs = 5

frequencies = [16., 31.5, 63., 125., 250., 500., 1000., 2000., 4000., 8000.]
directories = ['f{:.1f}'.format(freq) for freq in frequencies][:num_of_freqs + 1]

directories = ['f1000.0']
directories = ['f500.0']
directories = ['f16.0']

for directory in directories:
    f = directory[1:]
    # X = np.genfromtxt('results/f{}/r.csv'.format(f), delimiter=';')[1:]
    # Z = np.genfromtxt('results/f{}/result.csv'.format(f), delimiter=';')[1:].transpose()
    X = np.genfromtxt('results/f{}/r.csv'.format(f), delimiter=';')
    Y = np.genfromtxt('results/f{}/z.csv'.format(f), delimiter=';')
    Z = np.genfromtxt('results/f{}/result.csv'.format(f), delimiter=';').transpose()

    plot_contour(X, Y, Z, 200, cmap='Spectral', x_label='r [m]', y_label='z [m]',
                 title='Sound Pressure Level [dB] for frequency {}Hz'.format(f),
                 filename='results/plots/{}.png'.format(directory))

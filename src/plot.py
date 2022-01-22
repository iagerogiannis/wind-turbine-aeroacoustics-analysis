import os
import pandas as pd

from lib.output.plots import *
from lib.algorithms import *

from lib.aeroacoustics import *


def plot(frequency, h, results_dir):

    print('Creating plots...', end='', flush=True)

    r = np.genfromtxt('{}/r.csv'.format(results_dir), delimiter=';')[1:]
    z = np.genfromtxt('{}/z.csv'.format(results_dir), delimiter=';')
    SPL = np.genfromtxt('{}/SPL.csv'.format(results_dir), delimiter=';')[1:].transpose()

    if r.shape[0] != SPL.shape[1]:
        r = r[:-1]

    h_index = np.argmax(z > h)

    SPL_according_to_r = np.array([np.interp(h, [z[h_index - 1], z[h_index]],
                                             [SPL[h_index - 1][i], SPL[h_index][i]]) for i in range(SPL.shape[1])])

    plot_scatter([r, SPL_according_to_r], title='Sound Pressure Level [dB] for frequency {}Hz'.format(str(frequency)),
                 x_label='r [m]', y_label='SPL [dB]',
                 filename='{}/SPL_of_r.png'.format(results_dir))

    plot_contour(r, z, SPL, 200, z_max_percentage=.7, cmap='Spectral_r', x_label='r [m]', y_label='z [m]',
                 title='Sound Pressure Level [dB] for frequency {}Hz'.format(str(frequency)),
                 filename='{}/contour_with_layer.png'.format(results_dir))

    plot_contour(r, z, SPL, 200, z_max_percentage=.7, y_max=200., cmap='Spectral_r', x_label='r [m]', y_label='z [m]',
                 title='Sound Pressure Level [dB] for frequency {}Hz'.format(str(frequency)),
                 filename='{}/contour.png'.format(results_dir))

    print('', end='\r')
    print('Plots created')


def plot_totals(h, results_dir):
    def read_Lw(dir):
        f = open("{}\\Lw.dat".format(dir), "r")
        return float(f.read())

    def write_file(filename, data):
        with open(filename, 'w') as f:
            f.write(str(data))

    data = []
    directories = os.walk(results_dir)
    for dir in directories:
        directory = os.path.normpath(dir[0]).split(os.sep)
        if len(directory) == 4 and directory[2][0] == 'f':
            f = float(directory[2][1:])
            theta = float(directory[3][5:])
            Lw = read_Lw(dir[0])
            SPL = np.genfromtxt('{}/SPL.csv'.format(dir[0]), delimiter=';')[1:].transpose()
            z = np.genfromtxt('{}/z.csv'.format(dir[0]), delimiter=';')
            r = np.genfromtxt('{}/r.csv'.format(dir[0]), delimiter=';')[1:]
            h_index = np.argmax(z > h)
            SPL_of_r = np.array([np.interp(
                h, [z[h_index - 1], z[h_index]], [SPL[h_index - 1][i], SPL[h_index][i]]) for i in range(SPL.shape[1])])
            if r.shape[0] != SPL.shape[1]:
                r = r[:-1]
            data.append({
                "frequency": f,
                "theta": theta,
                "Lw": Lw,
                "r": r,
                "SPL_of_r": SPL_of_r,
                "SPL@receiver": SPL_of_r[-1]
            })

            pd.DataFrame({
                "r [m]": r,
                "SPL [dB]": SPL_of_r
            }).to_csv('{}/SPL_of_r.csv'.format(dir[0]), sep=';', encoding='utf-8')

    thetas = list(set([item['theta'] for item in data if 'theta' in item]))

    for theta in thetas:
        f = [item['frequency'] for item in data if item['theta'] == theta]
        SPL_at_receiver = [item['SPL@receiver'] for item in data if item['theta'] == theta]
        SPL_A_weighted = apply_A_weighting(SPL_at_receiver)
        SPL_eq = equivalent_level(SPL_at_receiver)
        Lw = [item['Lw'] for item in data if item['theta'] == theta]

        SPL_of_r = [item['SPL_of_r'] for item in data if item['theta'] == theta]
        r = [item['r'] for item in data if item['theta'] == theta]

        bubble_sort(f, [SPL_at_receiver, Lw, SPL_of_r, r])

        SPL_of_r_total = []
        for i in range(len(SPL_of_r)):
            SPL_of_r_total.append(r[i])
            SPL_of_r_total.append(SPL_of_r[i])

        plots_dir = '{}/total/theta{}'.format(results_dir, str(int(theta)))

        if not os.path.exists(plots_dir):
            os.makedirs(plots_dir)

        pd.DataFrame({
            "Frequency [Hz]": f,
            "Lw [dB]": Lw,
            "SPL [dB]": SPL_at_receiver,
            "SPL (A-weighted) [dB]": SPL_A_weighted
        }).to_csv('{}/data.csv'.format(plots_dir), sep=';', encoding='utf-8')

        write_file('{}/SPL_eq.dat'.format(plots_dir), SPL_eq)

        plot_scatter([f, SPL_at_receiver, f, SPL_A_weighted, f, [SPL_eq for i in range(len(SPL_A_weighted))]],
                     x_label='Frequency [Hz]', y_label='SPL [dB]', legend=['SLP', 'SLP (A-weighted)', 'SLP (equivalent)'],
                     title='Sound Pressure Level',
                     filename='{}/SPL.png'.format(plots_dir))

        plot_scatter([f, SPL_at_receiver, f, Lw],
                     x_label='Frequency [Hz]', y_label='SPL [dB]', legend=['Lp', 'Lw'],
                     title='Sound Pressure Level compared to Sound Power Level',
                     filename='{}/SPL_comparison.png'.format(plots_dir))

        plot_scatter(SPL_of_r_total,
                     x_label='r [m]', y_label='SPL [dB]', legend=['f = {}Hz'.format(f_i) for f_i in f],
                     title='Sound Pressure Level [dB] according to r'.format(h),
                     filename='{}/SPL_of_r.png'.format(plots_dir))

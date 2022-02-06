import os
import pandas as pd
import numpy as np

from src.file_manager import read_value_from_file
from src.output.plot.lib import plot_scatter


def plot_spectrums_combined(totals_dir, f_to_plot=None):

    SPL_at_receiver = []
    SPL_A_weighted = []
    SPL_eq_array = []

    directories = os.walk(totals_dir)
    for dir_ in directories:
        total_results_dir = dir_[0]
        directory = os.path.normpath(total_results_dir).split(os.sep)
        if directory[-1][:5] == 'theta':
            data = pd.read_csv('{}/data.csv'.format(total_results_dir), sep=';')

            f = np.array(data['Frequency [Hz]'])

            SPL_at_receiver.append(np.array(data['SPL [dB]']))
            SPL_A_weighted.append(np.array(data['SPL (A-weighted) [dB]']))
            SPL_eq = read_value_from_file(total_results_dir, 'SPL_eq.dat')
            SPL_eq_array.append([SPL_eq for _ in range(len(SPL_A_weighted[-1]))])

    plot_scatter([f, SPL_at_receiver[0], 'b', f, SPL_A_weighted[0], 'y', f, SPL_eq_array[0], 'g',
                  f, SPL_at_receiver[1], 'b--', f, SPL_A_weighted[1], 'y--', f, SPL_eq_array[1], 'g--'],
                 x_label='Frequency [Hz]', y_label='SPL [dB]',
                 legend=['SPL (0 deg)', 'SPL (A-weighted) (0 deg)', 'SPL (equivalent) (0 deg)',
                         'SPL (180 deg)', 'SPL (A-weighted) (180 deg)', 'SPL (equivalent) (180 deg)'],
                 title='Sound Pressure Level',
                 filename='{}/SPL.png'.format(totals_dir))

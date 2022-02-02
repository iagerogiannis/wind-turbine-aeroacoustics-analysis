import os
import pandas as pd
import numpy as np

from src.file_manager import read_value_from_file
from ..lib import plot_scatter


def plot_spectrum(totals_dir, f_to_plot=None):

    directories = os.walk(totals_dir)
    for dir_ in directories:
        total_results_dir = dir_[0]
        directory = os.path.normpath(total_results_dir).split(os.sep)
        if len(directory) == 4:
            data = pd.read_csv('{}/data.csv'.format(total_results_dir), sep=';')

            f = np.array(data['Frequency [Hz]'])

            if f_to_plot is None:
                f_to_plot = f

            Lw = np.array(data['Lw [dB]'])
            SPL_at_receiver = np.array(data['SPL [dB]'])
            SPL_A_weighted = np.array(data['SPL (A-weighted) [dB]'])
            SPL_eq = read_value_from_file(total_results_dir, 'SPL_eq.dat')
            SPL_eq_array = [SPL_eq for _ in range(len(SPL_A_weighted))]

            plot_scatter([f, SPL_at_receiver, f, SPL_A_weighted, f, SPL_eq_array],
                         x_label='Frequency [Hz]', y_label='SPL [dB]',
                         legend=['SPL', 'SPL (A-weighted)', 'SPL (equivalent)'],
                         title='Sound Pressure Level',
                         filename='{}/SPL.png'.format(total_results_dir))

            plot_scatter([f, SPL_at_receiver, f, Lw],
                         x_label='Frequency [Hz]', y_label='SPL [dB]', legend=['Lp', 'Lw'],
                         title='Sound Pressure Level compared to Sound Power Level',
                         filename='{}/SPL_comparison.png'.format(total_results_dir))

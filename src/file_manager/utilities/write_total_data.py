import os
import pandas as pd

from src.aeroacoustics import *
from src.algorithms import *
from ..lib import write_file


def write_total_data(results_dir, data):

    thetas = list(set([item['theta'] for item in data if 'theta' in item]))

    for theta in thetas:
        f = [item['frequency'] for item in data if item['theta'] == theta]
        Lw = [item['Lw'] for item in data if item['theta'] == theta]
        SPL_at_receiver = [item['SPL@receiver'] for item in data if item['theta'] == theta]
        SPL_A_weighted = apply_A_weighting(SPL_at_receiver)
        SPL_eq = equivalent_level(SPL_at_receiver)

        SPL_of_r = [item['SPL_of_r'] for item in data if item['theta'] == theta]
        r = [item['r'] for item in data if item['theta'] == theta]

        bubble_sort(f, [SPL_at_receiver, Lw, SPL_of_r, r])

        total_results_dir = '{}/total/theta{}'.format(results_dir, str(int(theta)))

        if not os.path.exists(total_results_dir):
            os.makedirs(total_results_dir)

        write_file('{}/SPL_eq.dat'.format(total_results_dir), SPL_eq)

        pd.DataFrame({
            "Frequency [Hz]": f,
            "Lw [dB]": Lw,
            "SPL [dB]": SPL_at_receiver,
            "SPL (A-weighted) [dB]": SPL_A_weighted
        }).to_csv('{}/data.csv'.format(total_results_dir), sep=';', index=False, encoding='utf-8')

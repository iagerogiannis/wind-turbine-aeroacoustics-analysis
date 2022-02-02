import os
import pandas as pd
import numpy as np

from ..lib import read_value_from_file
from .generate_SPL_of_r import generate_SPL_of_r
from .read_case_dir import read_case_dir

"""
If there is no value for h, then SPL_of_r.csv get read. Else new SPL of r
gets generated and SPL_of_r.csv gets replaced with the new values.
"""


def read_and_generate_data(results_dir, h=None):
    data = []
    directories = os.walk(results_dir)
    for dir_ in directories:
        case_dir = dir_[0]
        directory = os.path.normpath(case_dir).split(os.sep)
        if directory[-2][0] == 'f' and directory[-1][:5] == 'theta':
            f = float(directory[-2][1:])
            theta = float(directory[-1][5:])
            Lw = read_value_from_file(case_dir, 'Lw.dat')

            if not h:
                SPL_of_r_data = pd.read_csv('{}/SPL_of_r.csv'.format(case_dir), sep=';')
                r = np.array(SPL_of_r_data["r [m]"])
                SPL_of_r = np.array(SPL_of_r_data["SPL [dB]"])
            else:
                r, z, SPL = read_case_dir(case_dir)
                SPL_of_r = generate_SPL_of_r(z, SPL, h)

                pd.DataFrame({
                    "r [m]": r,
                    "SPL [dB]": SPL_of_r
                }).to_csv('{}/SPL_of_r.csv'.format(case_dir), sep=';', index=False, encoding='utf-8')

            SPL_at_receiver = SPL_of_r[-1]

            data.append({
                "frequency": f,
                "theta": theta,
                "Lw": Lw,
                "r": r,
                "SPL_of_r": SPL_of_r,
                "SPL@receiver": SPL_at_receiver
            })

    return data

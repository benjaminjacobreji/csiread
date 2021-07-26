"""ESP32-CSI-Tool

Read esp32 csi files flexibly.
"""

import numpy as np
import pandas as pd
from timeit import default_timer


def read_esp32(file):
    dtype = {'type': str, 'role': str, 'mac': str, 'rssi': int, 'rate': int,
             'sig_mode': int, 'mcs': int, 'bandwidth': int, 'smoothing': int,
             'not_sounding': int, 'aggregation': int,'stbc': int,
             'fec_coding': int, 'sgi': int, 'noise_floor': int,
             'ampdu_cnt': int, 'channel': int, 'secondary_channel': int,
             'local_timestamp': int, 'ant': int, 'sig_len': int,
             'rx_state': int, 'real_time_set': int, 'real_timestamp': float,
             'len': int, 'csi_data': object}
    names = list(dtype.keys())
    data = pd.read_csv(file, header=None, names=names, dtype=dtype,
                       usecols=['csi_data'], engine='c')

    # parse csi
    csi_string = ''.join(data['csi_data'].apply(lambda x: x.strip('[]')))
    csi = np.fromstring(csi_string, dtype=int, sep=' ').reshape(-1, 128)
    csi = csi[:, 1::2] + csi[:, ::2] * 1.j

    return csi

if __name__ == '__main__':
    last = default_timer()
    csifile = '../material/esp32/dataset/example_csi.csv'
    read_esp32(csifile)
    print(default_timer() - last, 's')

import numpy as np


def calc_pct_np(np_data):
    '''
    <numpy.ndarray> => new <numpy.ndarray>
    '''
    np_a = np.copy(np_data)
    np_a[np_a == 0] = np.finfo(float).eps # | 0.000000001
    return np.diff(np_a, axis=0) / np.abs(np_a[:-1])  # * 100


def convert_pctcum_np(np_data):
    '''
    NOTE! IN PLACE!

    price <numpy.ndarray> => pctcum <numpy.ndarray>
    '''

    if np_data.ndim == 1:
        tot_sym = 1
        len_data = np_data.shape[0]
    else:
        len_data, tot_sym = np_data.shape

    """ pctchg
    for s in range(0, tot_sym):
        for i in range(len_data-1, 0, -1):
            #if np_data[i-1,s] == 0:
            #    np_data[i,s]
            np_data[i,s] = (np_data[i,s] - np_data[i-1,s])/np_data[i-1,s]
    return np_data[1:,:]
    """
    if tot_sym == 1:
        for i in range(1, len_data):
            if np_data[0] == 0:
                np_data[i] = (np_data[i] - np.finfo(float).eps)/np.finfo(float).eps
            else:
                np_data[i] = (np_data[i] - np_data[0])/np_data[0]

        return np_data[1:,]

    for s in range(0, tot_sym):
        for i in range(1, len_data):
            if np_data[0,s] == 0:
                np_data[i,s] = (np_data[i,s] - np.finfo(float).eps)/np.finfo(float).eps
            else:
                np_data[i,s] = (np_data[i,s] - np_data[0,s])/np_data[0,s]

    return np_data[1:,]

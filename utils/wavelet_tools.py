
import pandas as pd
import numpy as np
import pywt

def decompose_wavelet_components(data, wavelet='db6', level=6):
    T2 = data - np.mean(data)
    coeffs = pywt.wavedec(T2, wavelet, level=level)
    bands = {}

    for name, idx in [('low_freq', level), ('mid_freq', level-1), ('high_freq', level-2)]:
        selected = [c if i == idx else np.zeros_like(c) for i, c in enumerate(coeffs)]
        recon = pywt.waverec(selected, wavelet)
        bands[name] = recon[:len(data)]

    return bands

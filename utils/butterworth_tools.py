
import numpy as np
import pandas as pd
from scipy.signal import butter, sosfiltfilt

def butter_bandpass_filter(data, fs, lowcut, highcut, order=2):
    nyq = 0.5 * fs
    sos = butter(order, [lowcut / nyq, highcut / nyq], btype='band', output='sos')
    return sosfiltfilt(sos, data)

def apply_named_bands(time_array, signal_array):
    '''
    Applies Butterworth bandpass filters for predefined frequency bands:
    - 3-day (0.24–0.38 cpd)
    - 7-day (0.09–0.18 cpd)
    - 1.5-day (0.52–0.74 cpd)

    Returns:
        Dictionary of {band_label: filtered_signal_array}
    '''
    fs = 1.0 / (time_array[1] - time_array[0])
    bands = {
        "3-day": (0.24, 0.38),
        "7-day": (0.09, 0.18),
        "1.5-day": (0.52, 0.74)
    }

    filtered = {}
    for label, (low, high) in bands.items():
        filtered[label] = butter_bandpass_filter(signal_array, fs, low, high)

    return filtered

def summarize_band(band_signal):
    '''
    Computes summary stats (max, min, std) for a filtered signal band.
    '''
    return {
        "max": float(np.max(band_signal)),
        "min": float(np.min(band_signal)),
        "std": float(np.std(band_signal))
    }

def export_filtered_csv(time_array, band_signals, prefix="butter"):
    '''
    Saves each filtered band to CSV using the provided prefix.
    '''
    for label, signal in band_signals.items():
        df = pd.DataFrame({"time": time_array, label: signal})
        df.to_csv(f"{prefix}_{label.replace('-', 'd')}.csv", index=False)

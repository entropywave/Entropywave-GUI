
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt
from numpy import nanmax, nanmin, isnan

# Load dataset
df = pd.read_csv("t2_multi_injection.csv")
time = df["Time_days"].values
T2_raw = df["Injected_T2_ns"].values
fs = 1 / (time[1] - time[0])
T2 = T2_raw - np.mean(T2_raw)

# Safe Butterworth bandpass filter using second-order sections
def safe_bandpass_filter(data, fs, lowcut, highcut, order=2):
    nyq = 0.5 * fs
    try:
        sos = butter(order, [lowcut / nyq, highcut / nyq], btype='band', output='sos')
        filtered = sosfiltfilt(sos, data)
        if np.any(np.isnan(filtered)) or np.allclose(filtered, 0):
            raise ValueError("Filtered output is NaN or zeroed.")
        return filtered
    except Exception as e:
        print(f"⚠️ Filter failed for band {lowcut:.3f}–{highcut:.3f} cpd: {e}")
        return np.full_like(data, np.nan)

# Define safer, slightly wider filter bands
filters = {
    "3-day": (0.24, 0.38),
    "7-day": (0.09, 0.18),
    "1.5-day": (0.52, 0.74)
}

# Filter and analyze
components_raw = {}
for label, (low, high) in filters.items():
    filtered = safe_bandpass_filter(T2, fs, low, high)
    components_raw[label] = filtered
    print(f"\n[{label} band] Filter {low:.3f}–{high:.3f} cycles/day")
    if not np.any(isnan(filtered)):
        print(f"  Max: {nanmax(filtered):.6f}, Min: {nanmin(filtered):.6f}, Std: {np.nanstd(filtered):.6f}")
    else:
        print("  Output is NaN — skipped")

# Plot raw filtered signals
plt.figure(figsize=(12, 5))
for label, signal in components_raw.items():
    if not np.any(isnan(signal)):
        plt.plot(time, signal, label=label)
plt.xlabel("Time (days)")
plt.ylabel("Filtered Amplitude")
plt.title("Raw Filtered Signal Components (Safe Butterworth)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Normalize and overlay if valid
plt.figure(figsize=(12, 5))
for label, signal in components_raw.items():
    if not np.any(isnan(signal)):
        norm_signal = signal / nanmax(np.abs(signal))
        plt.plot(time, norm_signal, label=label)
plt.xlabel("Time (days)")
plt.ylabel("Normalized Amplitude")
plt.title("Normalized Overlay of Filtered Components (Safe Butterworth)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

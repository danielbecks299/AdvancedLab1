import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.fft import fft, fftfreq
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

df = pd.read_csv('data.csv')

time = df['time']
photo_reading = df['A0']

dt = np.mean(np.diff(time))  
n = len(photo_reading)        

fft_values = np.abs(np.fft.fft(photo_reading))
fft_freqs = np.abs(np.fft.fftfreq(n, d=dt))
mags = np.abs(fft_values)

peaks, _ = find_peaks(np.abs(fft_values), height=10000)

print(fft_freqs[peaks])

# Create side-by-side plots (1 row, 2 columns)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Time domain raw data
ax1.plot(time, photo_reading, color='tab:blue')
ax1.set_title('Time Domain Signal')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('A0 Reading')
ax1.grid(True)

# Plot 2: Frequency domain FFT with peaks
ax2.plot(fft_freqs, fft_values, color='b', label='FFT Magnitude')
ax2.plot(
    fft_freqs[peaks],
    fft_values[peaks],
    'x',
    color='red',
    markersize=8,
    label='Peaks',
)
ax2.set_title('Frequency Spectrum (FFT)')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("my_plot.pdf", bbox_inches="tight")
plt.show()


# start_index = 200 

# clean_freqs = fft_freqs[start_index:]
# clean_magnitudes = mags[start_index:]

# df = clean_freqs[1] - clean_freqs[0]


# min_distance_indices = int(1 / df)

# peak_indices, _ = find_peaks(
#     clean_magnitudes,
#     distance=min_distance_indices,
#     prominence=6000,   
#     height=4000        
# )

# useful_frequencies = clean_freqs[peak_indices]
# useful_magnitudes = clean_magnitudes[peak_indices]

#plt.plot(useful_frequencies, useful_magnitudes, "x")

# print(useful_frequencies)
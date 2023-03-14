import numpy as np
import matplotlib.pyplot as plt
import scipy.io.wavfile as wavfile

# Load the .wav file
sample_rate, data = wavfile.read('sun.wav')

# Calculate the Fourier transform
fft = np.fft.fft(data)
freqs = np.fft.fftfreq(len(data)) * sample_rate

# Find the top 10 frequencies
abs_fft = np.abs(fft)
top_10_indices = np.argsort(abs_fft)[::-1][:10]
top_10_freqs = freqs[top_10_indices]
top_10_magnitudes = abs_fft[top_10_indices]

# Print the top 10 frequencies
print("Top 10 Frequencies:")
for i in range(10):
    print(f"{i+1}. {top_10_freqs[i]:.2f} Hz with magnitude {top_10_magnitudes[i]:.2f}")

# Plot the frequency spectrum
plt.plot(freqs, abs_fft)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Frequency Spectrum')
plt.show()

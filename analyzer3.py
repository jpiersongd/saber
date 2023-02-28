import wave
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

# Open the WAV file
filename = 'saber.wav'
with wave.open(filename, 'r') as wav_file:

    # Extract raw audio from the WAV file
    signal = wav_file.readframes(-1)
    signal = np.frombuffer(signal, dtype='int16')

    # Get the sample rate and duration of the WAV file
    sample_rate = wav_file.getframerate()
    duration = len(signal) / sample_rate

    # Create a time array
    time = np.linspace(0, duration, len(signal))

    # Perform Fourier transform on the signal
    freqs = fftfreq(len(signal)) * sample_rate
    fft_signal = fft(signal)

    # Get the magnitudes of the frequencies
    magnitudes = np.abs(fft_signal)

    # Set the frequency range to display
    x = 10  # Lower frequency limit
    y = 200  # Upper frequency limit
    bucket_size = 10  # Frequency bucket size
    num_buckets = int((y - x) / bucket_size)  # Number of frequency buckets
    buckets = np.linspace(x, y, num_buckets + 1)  # Create frequency buckets
    mask = np.zeros_like(freqs, dtype=bool)  # Initialize mask
    for i in range(num_buckets):
        mask |= (freqs >= buckets[i]) & (freqs < buckets[i+1])
    freqs_masked = freqs[mask]
    magnitudes_masked = magnitudes[mask]

    # Create a table of frequencies and their corresponding magnitudes
    table = np.column_stack((freqs_masked, magnitudes_masked))
    table_sorted = table[np.argsort(table[:, 1])[::-1]]  # Sort table by magnitudes
    top_frequencies = table_sorted[:10]  # Get top 10 frequencies

    # Plot the spectrum as a graph
    plt.plot(freqs_masked, magnitudes_masked)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    # Set the frequency range and tick marks of the x-axis
    plt.xlim([x, y])
    plt.xticks(np.arange(x, y+1, 10))
    plt.grid(True)

    plt.show()

    # Print the table of frequencies and magnitudes
    print('Top 10 Frequencies (Hz)\tMagnitude')
    for row in top_frequencies:
        print(f'{row[0]:.1f}\t\t\t{row[1]:.2f}')


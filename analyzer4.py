import wave
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
from tabulate import tabulate

# Open the WAV file
filename = 'sun.wav'
print(filename)
with wave.open(filename, 'r') as wav_file:

    # Extract raw audio from the WAV file
    signal = wav_file.readframes(-1)
    signal = np.frombuffer(signal, dtype='int16')

    #Get a few interesting fields
    channels = wav_file.getnchannels()  #-- returns number of audio channels (1 for mono, 2 for stereo)
    samplewidth = wav_file.getsampwidth()  #-- returns sample width in bytes
    print('channels={0:0.2F} samplewidth={1:0.2F}'.format(channels, samplewidth))
      
    # Get the sample rate and duration of the WAV file
    sample_rate = wav_file.getframerate()
    duration = len(signal) / sample_rate
    print('duration={0:0.2F} sampleRate={1:0.2F} signalLength={2:0.2F}'.format(duration, sample_rate, len(signal)))

    # Create a time array
    time = np.linspace(0, duration, len(signal))

    # Perform Fourier transform on the signal
    freqs = fftfreq(len(signal)) * sample_rate
    print(freqs)
    fft_signal = fft(signal)

    # Get the magnitudes of the frequencies
    magnitudes = np.abs(fft_signal)

<<<<<<< HEAD
    # Set the frequency range to display
    x = 0  # Lower frequency limit
=======
    # Set the i frequency range to display
    x = 10  # Lower frequency limit
>>>>>>> 0b3b76171c56fd146ed6c8f04a08a4e042850ff4
    y = 300 # Upper frequency limit
    mask = (freqs > x) & (freqs < y)
    freqs_masked = freqs[mask]
    magnitudes_masked = magnitudes[mask]

    # Create a table of frequencies and their corresponding magnitudes
    table = []
    bucket_size = 10
    for i in range(int((y - x) / bucket_size)):
        lower_freq = i * bucket_size + x
        upper_freq = lower_freq + bucket_size
        freq_mask = (freqs_masked >= lower_freq) & (freqs_masked < upper_freq)
        bucket_magnitudes = magnitudes_masked[freq_mask]
        if len(bucket_magnitudes) > 0:
            max_magnitude = np.max(bucket_magnitudes)
            max_freq = freqs_masked[freq_mask][np.argmax(bucket_magnitudes)]
            table.append([max_freq, max_magnitude])

    # Sort the table by descending magnitude and select the top 10 frequencies
    table.sort(key=lambda x: x[1], reverse=True)
    table = table[:10]

    # Print the table of frequencies and magnitudes
    headers = ['Frequency (Hz)', 'Magnitude']
    print(tabulate(table, headers=headers))

    # Plot the spectrum as a graph
    plt.plot(freqs_masked, magnitudes_masked)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    # Set the frequency range and tick marks of the x-axis
    plt.xlim([x, y])
    plt.xticks(np.arange(x, y+1, 10))
    plt.grid(True)

    plt.show()

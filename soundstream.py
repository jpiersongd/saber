import time
import numpy as np
import pyaudio

p = pyaudio.PyAudio()

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 5.0  # in seconds, may be float
f1 = 440.0  # sine frequency, Hz, may be float
f2 = 128.0  # second sine frequency, Hz, may be float

# generate samples for first frequency, note conversion to float32 array
samples1 = (np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs)).astype(np.float32)

# generate samples for second frequency
samples2 = (np.sin(2 * np.pi * np.arange(fs * duration) * f2 / fs)).astype(np.float32)

# per @yahweh comment explicitly convert to bytes sequence
output_bytes1 = (volume * samples1).tobytes()

# convert samples for second frequency to bytes
output_bytes2 = (volume * samples2).tobytes()

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)

# play first frequency. May repeat with different volume values (if done interactively)
start_time = time.time()
stream.write(output_bytes1)
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

# update stream with second frequency
start_time = time.time()
stream.write(output_bytes2)
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

stream.stop_stream()
stream.close()

p.terminate()

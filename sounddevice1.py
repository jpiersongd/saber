import time
import numpy as np
import sounddevice as sd

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 5.0  # in seconds, may be float
f = 440.0  # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

# normalize samples to range [-1.0, 1.0]
samples /= np.max(np.abs(samples))

# play sound
start_time = time.time()
sd.play(volume * samples, fs)
sd.wait()  # wait for sound to finish
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

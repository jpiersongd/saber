import numpy as np
import sounddevice as sd


def callback(indata, outdata, frames, time):
    print(flush=True)
    t = (time + np.arange(frames)) / fs
    t = t.reshape(-1, 1)
    outdata[:] = np.sin(2 * np.pi * F1 * t)
    
# Set up the parameters
volume = 0.5
fs = 44100
blocksize = 44100
duration = 5.0
f1 = 41.0
f2 = 71.0
status = "none"

# Create the combined signal
combined_signal = volume * np.sin(2 * np.pi * f1 * np.arange(fs * duration) / fs)

# Play the combined signal using the callback function
stream = sd.OutputStream(callback=callback, blocksize=blocksize)
with stream:
    sd.play(combined_signal, blocking=True)

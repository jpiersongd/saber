import sounddevice as sd
import numpy as np
import threading
import time

# Define the parameters for the sounds
fs = 44100
duration = 5.0
f1 = 43.0
f2 = 71.0

# Generate the samples for the first frequency
samples1 = np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs).astype(np.float32)

# Generate the samples for the second frequency
samples2 = np.sin(2 * np.pi * np.arange(fs * duration) * f2 / fs).astype(np.float32)

# Define the functions to play the sounds
def play_sound1():
    sd.play(samples1, fs, loop=True)
    #sd.wait()

def play_sound2():
    sd.play(samples2, fs)
    sd.wait()

# Start playing the sounds concurrently using threads
thread1 = threading.Thread(target=play_sound1)
thread1.start()
time.sleep(5)
thread2 = threading.Thread(target=play_sound2)
thread2.start()

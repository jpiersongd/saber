import time
import numpy as np
import sounddevice as sd

# set print options to display floats with fixed-point notation
np.set_printoptions(precision=6, suppress=True)

volume = 0.5  # range [0.0, 1.0]
fs = 44100  # sampling rate, Hz, must be integer
duration = 5.0  # in seconds, may be float
f1 = 440.0  # initial sine frequency, Hz, may be float
f2 = 71.0   # new sine frequency, Hz, may be float
fade_time = 0.1 # time for fade-in/out transition between frequencies
leading_edge_time = 0.1 # time to extract from the first set of samples just before the new frequency starts

# generate initial samples, note conversion to float32 array
samples1 = (np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs)).astype(np.float32)

# calculate indices of samples to extract from the leading edge of samples1
leading_edge_samples = int(leading_edge_time * fs)
leading_edge_idx = len(samples1) - leading_edge_samples

# generate new samples with new frequency and duration
duration2 = duration - fade_time * 2
samples2 = (np.sin(2 * np.pi * np.arange(fs * duration2) * f2 / fs)).astype(np.float32)

# concatenate the two sets of samples with fade-in/out transitions
fade_samples = np.linspace(0, 1, int(fade_time * fs))
fade_in = fade_samples ** 2  # quadratic fade-in
fade_out = fade_samples[::-1] ** 2  # quadratic fade-out
samples = np.concatenate([
    samples1[:len(samples1) - len(samples2) - leading_edge_samples], # before leading edge
    samples1[len(samples1) - len(samples2) - leading_edge_samples:-len(fade_out)],
    fade_out * samples1[-len(fade_out):] + fade_in * samples2[:len(fade_in)],
    samples2,
    fade_out * samples2[-len(fade_out):] + fade_in * samples1[len(samples2):len(samples2)+len(fade_in)],
    samples1[len(samples2)+len(fade_in):] # after fade-in
])

# normalize samples to range [-1.0, 1.0]
samples /= np.max(np.abs(samples))

# print leading edge of samples1
print("Leading edge of samples1: ", np.array2string(samples1[leading_edge_idx:leading_edge_idx+leading_edge_samples], separator=', '))

# play sound
start_time = time.time()
sd.play(volume * samples, fs)
sd.wait()  # wait for sound to finish
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

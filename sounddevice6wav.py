import time
import numpy as np
import sounddevice as sd
from scipy.io import wavfile
import wave

# Set up the parameters
volume = 0.3
fs = 44100
duration = 5.0
f1 = 71.1233
f2 = 128.865
overlap = 0.1  # 10% overlap between the two sets of samples

# Generate the samples for the first frequency
samples1 = np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs).astype(np.float32)[1:]

# Generate the samples for the second frequency with some overlap
samples2 = np.sin(2 * np.pi * np.arange(fs * duration * overlap, fs * (duration * (1 + overlap))) * f2 / fs).astype(np.float32)

# Combine the two sets of samples
samples = np.concatenate((samples1, samples2))

# Check if the leading edge is all zeros and regenerate the samples if necessary
while np.all(samples[:int(fs * overlap)] == 0):
    samples1 = np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs).astype(np.float32)[1:]
    samples2 = np.sin(2 * np.pi * np.arange(fs * duration * overlap, fs * (duration * (1 + overlap))) * f2 / fs).astype(np.float32)
    samples = np.concatenate((samples1, samples2))

# Print the leading edge of the samples
leading_edge = samples[:int(fs * overlap)]
np.set_printoptions(threshold=100)
print("Leading edge of samples: {}".format(leading_edge[:100]))

# Print the leading edge of the samples2
leading_edge2 = samples2[:int(fs * overlap)]
np.set_printoptions(threshold=100)
print("Leading edge of samples: {}".format(leading_edge2[:100]))

# Save the samples to a .wav file
#wavfile.write("output.wav", fs, samples)

with wave.open("output.wav", "wb") as wavfile:
    wavfile.setparams((1, 2, fs, len(samples), "NONE", "not compressed"))
    wavfile.writeframes(samples.astype(np.int16).tobytes())

# Play the samples
start_time = time.time()
sd.play(volume * samples, fs)
sd.wait()

print("Played sound for {:.2f} seconds".format(time.time() - start_time))

import time
import numpy as np
import sounddevice as sd

# Set up the parameters
volume = 0.5
fs = 44100
duration = 5.0
f1 = 440.0
f2 = 71.0
overlap = 0.1  # 10% overlap between the two sets of samples

# Generate the samples for the first frequency
samples1 = np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs).astype(np.float32)

# Generate the samples for the second frequency with some overlap
samples2 = np.sin(2 * np.pi * np.arange(fs * (duration * (1 + overlap))) * f2 / fs).astype(np.float32)
#samples2 = samples2[int(fs * duration * overlap):]
samples2 = samples2[6:]

# Combine the two sets of samples
samples = np.concatenate((samples1, samples2))

# Print the leading edge of the samples
leading_edge = samples[:int(fs * overlap*10)]
leading_edge = leading_edge[6:]  # Skip the first value
print("Leading edge of samples: {}".format(leading_edge))

# Play the samples
start_time = time.time()
sd.play(volume * samples[6:], fs)
sd.wait()
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

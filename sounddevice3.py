import time
import numpy as np
import sounddevice as sd

# Set up the parameters
volume = 0.5
fs = 44100
duration = 2.0
f1 = 43.0
f2 = 71.0  #71
overlap = 0.1  # 10% overlap between the two sets of samples

# Generate the samples for the first frequency
samples1 = np.sin(2 * np.pi * np.arange(fs * duration) * f1 / fs).astype(np.float32)

# Generate the samples for the second frequency
samples2 = np.sin(2 * np.pi * np.arange(fs * duration) * f2 / fs).astype(np.float32)


# Combine the two sets of samples
samples3 = np.concatenate((samples1, samples2))
samples4 = np.concatenate((samples3, samples3))

# Print the leading edge of the samples
leading_edge1 = samples1[:10]  # start of first tone
trailing_edge1 = samples1[-30:]  #last 20
leading_edge2 = samples2[:30]  # start of second tone
trailing_edge2 = samples2[-10:]
print("1st Leading edge of samples: \n{}".format(leading_edge1))
print("1st Trailing edge of samples: \n{}".format(trailing_edge1))
print("samples1 count: \n{}".format(len(samples1)))
print("Second Leading edge of samples: \n{}".format(leading_edge2))
print("Second Trailing edge of samples: \n{}".format(trailing_edge2))
print("samples2 count: \n{}".format(len(samples2)))
print("total count: \n{}".format(len(samples4)))

# Play the samples
start_time = time.time()
sd.play(volume * samples4[:], fs*4)
sd.wait()
sd.play(volume * samples4[:], fs*4)
sd.wait()
print("Played sound for {:.2f} seconds".format(time.time() - start_time))

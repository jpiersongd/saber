import time

import numpy as np
import pyaudio

p = pyaudio.PyAudio()

volume = 0.5  # range [0.0, 1.0]
sampleRate = 44100  # sampling rate, Hz, must be integer
duration = 50.0  # in seconds, may be float
f = 71.1233 # sine frequency, Hz, may be float
f2 = 128.865

# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sampleRate,
                output=True)

# generate samples, note conversion to float32 array
samples = (np.sin(2 * np.pi * np.arange(sampleRate * duration) * f / sampleRate)).astype(np.float32)

# per @yahweh comment explicitly convert to bytes sequence
output_bytes = (volume * samples).tobytes()

# generate samples, note conversion to float32 array
samples2 = (np.sin(2 * np.pi * np.arange(sampleRate * duration) * f2 / sampleRate)).astype(np.float32)

# per @yahweh comment explicitly convert to bytes sequence
output_bytes2 = (volume * samples2).tobytes()



# play. May repeat with different volume values (if done interactively)
start_time = time.time()
stream.write(output_bytes)
time.sleep(1)
#stream.write(output_bytes2)


print("Played sound for {:.2f} seconds".format(time.time() - start_time))

stream.stop_stream()
stream.close()

p.terminate()

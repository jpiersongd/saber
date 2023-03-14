import sounddevice as sd
import numpy as np
import time
start_time = time.monotonic()


F1 = 71

# Define the callback function to generate audio data
def callback(outdata, frames, time, status):
    if status:
        print(status, flush=True)
    rndoff = np.random.uniform(.5, 1.5)
    t = np.linspace(0, frames / fs, frames, False)
    outdata[:] = 0.5 * np.sin( rndoff * 2 * np.pi * 440 * t)[:, np.newaxis]
    #t = t.reshape(-1, 1)
    #outdata[:] = 0.5 * np.sin(rndoff * 2 * np.pi * F1 * t)
    
    # Print the leading edge of the samples
    leading_edge1 = outdata[:20]  # start of first tone
    #trailing_edge1 = outdata[-20:]  #last 20
    #print("1st Leading edge of samples: \n{}".format(leading_edge1))
    ##print("1st Trailing edge of samples: \n{}".format(trailing_edge1))
    #print("samples1 count: \n{}".format(len(outdata)))

# Set up the parameters for the audio playback
fs = 44100
duration = 15.0




# Start the audio playback using the callback function
with sd.OutputStream(channels=1, blocksize=int(fs), samplerate=fs, callback=callback):
    sd.sleep(int(fs))

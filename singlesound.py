import time
import pygame
import math
import numpy


# Initialize the audio
pygame.mixer.pre_init(44100, -16, 2, 2048)   #frequency, size, channels, buffer
pygame.mixer.init()
print("pygame mixer started")



# Define the sound creation function
def create_sound(frequency1, frequency2, volume):
    duration = 5000
    sample_rate = 44100
    num_samples = int(duration * sample_rate / 1000)

    sound_data = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        sound_sample1 = float(volume * numpy.sin(frequency1 * t * 2 * numpy.pi))
        sound_sample2 = float(volume * numpy.sin(frequency2 * t * 2 * numpy.pi))
        sound_data.append([sound_sample1, sound_sample2])
        
    sound_array = numpy.array(sound_data, dtype=numpy.int16)
    return sound_array

# Create a stereo sound with 2 channels
frequency1 = 440  # Hz
frequency2 = 880  # Hz
volume = 0.5
stereo_sound = create_sound(frequency1, frequency2, volume)

# Print the shape of the stereo sound array
print(stereo_sound.shape)  # Output: (7056, 2)

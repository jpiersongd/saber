import pygame
import numpy as np

# Set the frequency of the tone in Hz
freq = 71

# Initialize Pygame audio
# Initialize the audio
pygame.mixer.pre_init(44100, -16, 2, 2048)   #frequency, size, channels, buffer
pygame.mixer.init(frequency=44100, channels=2)

# Set the number of audio channels in the Pygame mixer
num_channels = pygame.mixer.get_num_channels()
print(num_channels)

# Create a 2-dimensional NumPy array with the desired frequency
arr = np.array([int(32767 * np.sin(2 * np.pi * freq * x / 44100)) for x in range(44100)])
arr_2d = np.tile(arr, (num_channels, 1)).T

# Ensure that the array is C-contiguous
arr_2d = np.ascontiguousarray(arr_2d)

# Create a new sound with the 2-dimensional array
sound = pygame.sndarray.make_sound(arr_2d)

# Play the sound continuously
sound.play(-1)

# Wait for the user to press a key
input("Press Enter to stop the tone...")

# Stop the sound and quit Pygame
sound.stop()
pygame.quit()

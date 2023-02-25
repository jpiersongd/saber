import time
import pygame
import math
import numpy


# Initialize the audio
pygame.mixer.pre_init(44100, -16, 16, 2048)   #frequency, size, channels, buffer
pygame.mixer.init()
print("pygame mixer started")


# Define the sound play function
def play_sound(): 
    volume = 1    
    frequency1 = 46

    
    #print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} \t'.format(frequency1, frequency2, frequency3, frequency4))

    channel1 = pygame.mixer.Channel(0)    
    sound1 = pygame.sndarray.make_sound(create_sound(frequency1, volume))
    channel1.play(sound1, loops=-1)



#Define the sound creation function
def create_sound(frequency, volume):
    duration = 160
    sample_rate = 44100
    num_samples = int(duration * sample_rate / 1000)

    sound_data = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        sound_sample = float(volume * math.sin(frequency * t * 2 * math.pi))
        #print(sound_sample)
        sound_data.append(sound_sample * 32767)
        
    # Ensure that the length of sound_data is evenly divisible by 2
    while len(sound_data) % 2 != 0:
        sound_data.append(0)
    
    sound_array = numpy.array(sound_data, dtype=numpy.int16)
    sound_array = numpy.reshape(sound_array, (-1, 2))
    #print(sound_array)
    
    return sound_array


# Start the main loop
is_recording = True
while True:
    if is_recording:
        # Play the sound
        play_sound()

    # Delay for a short time
    time.sleep(0)

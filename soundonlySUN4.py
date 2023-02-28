import time
import pygame
import math
import numpy

duration = 500
sample_rate = 44100
num_samples = int(duration * sample_rate / 1000)
silence_duration = 5  # in milliseconds
silence_samples = int(silence_duration * sample_rate / 1000)

# Initialize the audio
pygame.mixer.pre_init(44100, -16, 2, 2048)   #frequency, size, channels, buffer
pygame.mixer.init()
print("pygame mixer started")


# Define the sound play function
def play_sound(): 
    volume = 1 
    frequency1 = 71.233
    frequency2 = 128.86
    
    #print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} \t'.format(frequency1, frequency2, frequency3, frequency4))

    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)  
     
    sound1 = pygame.sndarray.make_sound(create_sound(frequency1, volume*1))
    sound2 = pygame.sndarray.make_sound(create_sound(frequency2, volume*.5))

 # Play the sounds continuously
    channel1.play(sound1, loops=-1)
    channel2.play(sound2, loops=-1)

    time.sleep(duration)



#Define the sound creation function
def create_sound(frequency, volume):
    sound_data = []

    for i in range(num_samples):
        t = float(i) / sample_rate
        sound_sample = float(volume * math.sin(frequency * t * 2 * math.pi))
        volume_factor = min(1, i / (num_samples * .1)) ** 0.5   #fades in/out to reduce clicking
        sound_data.append(int(sound_sample * volume_factor * 32767))
        sound_data += [0,0]  # add silence at end

    # Ensure that the length of sound_data is evenly divisible by 2
    while len(sound_data) % 2 != 0:
        sound_data.append(0)

    sound_array = numpy.array(sound_data, dtype=numpy.int16)
    sound_array = numpy.reshape(sound_array, (-1, 2))

    return sound_array



# Start the main loop
is_recording = True
while True:
    if is_recording:
        # Play the sound
        play_sound()


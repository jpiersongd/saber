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
    frequency2 = 39
    frequency3 = 89
    frequency4 = 136
    frequency5 = 62
    frequency6 = 52
    frequency7 = 148
    frequency8 = 92
    
    print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} \t'.format(frequency1, frequency2, frequency3, frequency4))

    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)  
    channel3 = pygame.mixer.Channel(2)
    channel4 = pygame.mixer.Channel(3)
    channel5 = pygame.mixer.Channel(4)
    channel6 = pygame.mixer.Channel(5)
    channel7 = pygame.mixer.Channel(6)
    channel8 = pygame.mixer.Channel(7)
     
    sound1 = pygame.sndarray.make_sound(create_sound(frequency1, volume))
    sound2 = pygame.sndarray.make_sound(create_sound(frequency2, volume*1))
    sound3 = pygame.sndarray.make_sound(create_sound(frequency3, volume))
    sound4 = pygame.sndarray.make_sound(create_sound(frequency4, volume))
    sound5 = pygame.sndarray.make_sound(create_sound(frequency5, volume))
    sound6 = pygame.sndarray.make_sound(create_sound(frequency6, volume))
    sound7 = pygame.sndarray.make_sound(create_sound(frequency7, volume))
    sound8 = pygame.sndarray.make_sound(create_sound(frequency8, volume))

 # Play the sounds continuously
    channel1.play(sound1, loops=-1)
    channel2.play(sound2, loops=-1)
    channel3.play(sound3, loops=-1)
    channel4.play(sound4, loops=-1)
    channel5.play(sound5, loops=-1)
    channel6.play(sound6, loops=-1)
    channel7.play(sound7, loops=-1)
    channel8.play(sound8, loops=-1)


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
        sound_data.append(60)
    
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

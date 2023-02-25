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
    volume = .3  
    frequency1 = 71.233
    frequency2 = 128.86
    frequency3 = 0
    frequency4 = 0
    frequency5 = 0
    frequency6 = 0
    frequency7 = 0
    frequency8 = 0
    
    #print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} \t'.format(frequency1, frequency2, frequency3, frequency4))

    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)  
    #channel3 = pygame.mixer.Channel(2)
    #channel4 = pygame.mixer.Channel(3)
    #channel5 = pygame.mixer.Channel(4)
    #channel6 = pygame.mixer.Channel(5)
    #channel7 = pygame.mixer.Channel(6)
    #channel8 = pygame.mixer.Channel(7)
     
    sound1 = pygame.sndarray.make_sound(create_sound(frequency1, volume*1.37))
    sound2 = pygame.sndarray.make_sound(create_sound(frequency2, volume*1.3))
    #sound3 = pygame.sndarray.make_sound(create_sound(frequency3, volume*1.2))
    #sound4 = pygame.sndarray.make_sound(create_sound(frequency4, volume*1.157))
    #sound5 = pygame.sndarray.make_sound(create_sound(frequency5, volume))
    #sound6 = pygame.sndarray.make_sound(create_sound(frequency6, volume))
    #sound7 = pygame.sndarray.make_sound(create_sound(frequency7, volume))
    #sound8 = pygame.sndarray.make_sound(create_sound(frequency8, volume))

 # Play the sounds continuously
    channel1.play(sound1, loops=-1)
    channel2.play(sound2, loops=-1)
    #channel3.play(sound3, loops=-1)
    #channel4.play(sound4, loops=-1)
    #channel5.play(sound5, loops=-1)
    #channel6.play(sound6, loops=-1)
    #channel7.play(sound7, loops=-1)
    #channel8.play(sound8, loops=-1)
    time.sleep(duration)
    channel1.stop()
    channel2.stop()


#Define the sound creation function
def create_sound(frequency, volume):
    duration = 500  # each tone lasts for 100 ms
    sample_rate = 44100
    num_samples = int(duration * sample_rate / 1000)
    
    sound_data = []

    for i in range(num_samples):
        t = float(i) / sample_rate
        
        # Generate a sine wave with a frequency of 0.1 Hz
        # This will be used to modulate the main frequency
        modulation_frequency = .01
        modulation_wave = math.sin(modulation_frequency * t * 2 * math.pi)
        
        # Calculate the frequency of the main tone as the sum of the base frequency
        # and a modulation amount that is proportional to the amplitude of the modulation wave
        modulation_amount = 10  # adjust this value to control the degree of frequency modulation
        main_frequency = frequency + (modulation_amount * modulation_wave)
        
        # Generate the sound sample for the current time step using the modulated frequency
        sound_sample = float(volume * math.sin(main_frequency * t * 2 * math.pi))
        
        # Apply a fade-in and fade-out to the sound sample to reduce clicking
        fade_in_duration = 0.01
        fade_out_duration = 0.01
        fade_in_samples = int(fade_in_duration * sample_rate)
        fade_out_samples = int(fade_out_duration * sample_rate)
        if i < fade_in_samples:
            fade_factor = i / fade_in_samples
        elif i >= num_samples - fade_out_samples:
            fade_factor = (num_samples - i) / fade_out_samples
        else:
            fade_factor = 1.0
        sound_sample *= fade_factor
        
        # Convert the sound sample to a 16-bit integer and add it to the sound data
        sound_data.append(int(sound_sample * 32767))
        
    # Repeat the sound data to make a continuous sound
    num_repeats = int(sample_rate * 1.0 / duration)  # repeat the tone every 1 second
    sound_data *= num_repeats
    
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

    # Delay for a short time
    time.sleep(0)

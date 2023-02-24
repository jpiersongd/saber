import time
import pygame
import board
from Adafruit_BNO055 import BNO055
import RPi.GPIO as GPIO
import os
import math
import numpy

# Initialize the BNO055 sensor and stop if something went wrong.
sensor = BNO055.BNO055()
if not sensor.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = sensor.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')


# Initialize the GPIO pins
START_STOP_PIN = 23
MODE_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(START_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MODE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print("GPIO started")


# Initialize the audio
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
print("pygame mixer started")

#define a method to prorate input values between an output range
def prorate_output(value, low, high, low_value, high_value):
    if value < low:
        return low_value + (value - low) * (high_value - low_value) / (low - high)
    elif value > high:
        return high_value + (value - high) * (low_value - high_value) / (high - low)
    else:
        return low_value + (value - low) * (high_value - low_value) / (low - high)



# Define the sound play function
def play_sound(heading, roll, pitch, AccelX, AccelY, AccelZ): 
    volume = 1    
    pro_heading = abs(prorate_output(heading, 0, 360, 0, 1))
    pro_roll = abs(prorate_output(roll, 0, 360, 0, 1))
    pro_pitch = abs(prorate_output(pitch, 0, 360, 0, 1))

    frequencyA = 180 + (35* pro_heading)
    frequencyB = 181 + (48* pro_roll)
    frequencyC = 182 + (52* pro_pitch)
    frequencyD = 183 + (140* pro_heading)
    print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} pro_heading={4:0.2F} \t'.format(frequencyA, frequencyB, frequencyC, frequencyD, pro_heading))

    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)  
    channel3 = pygame.mixer.Channel(2)
    channel4 = pygame.mixer.Channel(3)
     
    sound1 = pygame.sndarray.make_sound(create_sound(frequencyA, volume))
    sound2 = pygame.sndarray.make_sound(create_sound(frequencyB, volume))
    sound3 = pygame.sndarray.make_sound(create_sound(frequencyC, volume))
    sound4 = pygame.sndarray.make_sound(create_sound(frequencyD, volume))

 # Play the sounds continuously
    channel1.play(sound1, loops=-1)
    channel2.play(sound2, loops=-1)
    channel3.play(sound3, loops=-1)
    channel4.play(sound4, loops=-1)

#35  <<<<  48  <<<<<<<<  52   62  70  90  140

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


# Define the start/stop function
def start_stop(channel):
    global is_recording
    is_recording = not is_recording
    if is_recording:
        print("Recording started")
    else:
        print("Recording stopped")
        #pygame.mixer.stop()

# Define the mode function
def mode(channel):
    pass

# Set up the GPIO interrupts
GPIO.add_event_detect(START_STOP_PIN, GPIO.FALLING, callback=start_stop, bouncetime=200)
GPIO.add_event_detect(MODE_PIN, GPIO.FALLING, callback=mode, bouncetime=200)

# Start the main loop
is_recording = True
# Read the Euler angles for heading, roll, pitch (all in degrees).
heading, roll, pitch = sensor.read_euler()
AccelX, AccelY, AccelZ = sensor.read_linear_acceleration()
while True:
    if is_recording:
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        #heading, roll, pitch = sensor.read_euler()
        #AccelX, AccelY, AccelZ = sensor.read_linear_acceleration()
        #temperature = (sensor.read_temp() * 2) +32
        #print(temperature)

        # Print everything out.
        #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\t AccelX={3} AccelY={4} AccelZ={5}'.format(heading, roll, pitch, AccelX, AccelY, AccelZ))

        # Play the sound
        play_sound(float(heading), float(roll), float(pitch), float(AccelX), float(AccelY), float(AccelZ))
        heading, roll, pitch = sensor.read_euler()
        AccelX, AccelY, AccelZ = sensor.read_linear_acceleration()

    # Delay for a short time
    time.sleep(0)

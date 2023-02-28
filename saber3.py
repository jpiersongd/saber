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


# Define the sound play function
def play_sound(heading, roll, pitch, AccelX, AccelY, AccelZ):
    #frequencyA = 261.63 * (abs(x) + abs(y) + abs(z)) / 30  #C4
    #frequencyB = 277.18 * (abs(x) + abs(y) + abs(z)) / 30  #C4#
    #frequencyC = 293.66 * (abs(x) + abs(y) + abs(z)) / 30  #D4
    #frequencyD = 311.13 * (abs(x) + abs(y) + abs(z)) / 30  #D4#
    #frequencyA = 83 * (abs(x) + abs(y) + abs(z)) / 30
    #frequencyB = 124 * (abs(x) + abs(y) + abs(z)) / 30
    #frequencyC = 147 * (abs(x) + abs(y) + abs(z)) / 30
    #frequencyD = 261 * (abs(x) + abs(y) + abs(z)) / 30
    
    varientHRP = min(max(abs(heading) + abs(roll) + abs(pitch), 65), 500) 
    varientAccel = min(max(abs(AccelX) * abs(AccelY) * abs(AccelZ), 0), 50)

    frequencyA = min(max(60 + varientHRP + varientAccel, 60), 500)
    frequencyB = min(max(98 + varientHRP + varientAccel, 98), 500)
    frequencyC = min(max(82 + varientHRP + varientAccel, 82), 500)
    frequencyD = min(max(65 + varientHRP + varientAccel, 65), 1500)
    duration = 100
    sample_rate = 44100
    num_samples = int(duration * sample_rate / 1000)
    volume = 1
    #print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} AccelX={4:0.2F} AccelY={5:0.2F} AccelZ={6:0.2F} varient={7:0.2F}  \t'.format(frequencyA, frequencyB, frequencyC, frequencyD, AccelX, AccelY, AccelZ, varient))
    print('freqA={0:0.2F} freqB={1:0.2F} freqC={2:0.2F} freqD={3:0.2F} varientHRP={4:0.2F} varientAccel={5:0.2F} \t'.format(frequencyA, frequencyB, frequencyC, frequencyD, varientHRP, varientAccel))

    create_sound(frequencyA, duration, sample_rate, num_samples, volume)
    time.sleep(0)
    create_sound(frequencyB, duration, sample_rate, num_samples, volume)
    time.sleep(0)
    create_sound(frequencyC, duration, sample_rate, num_samples, volume)
    time.sleep(0)
    create_sound(frequencyD, duration, sample_rate, num_samples, volume)
    pygame.time.wait(int(duration * 2))
    #sound.stop()


#Define the sound creation function
def create_sound(frequency, duration, sample_rate, num_samples, volume):
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
    sound = pygame.sndarray.make_sound(sound_array)

    # Play the sound
    sound.play()

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
while True:
    if is_recording:
        # Read the Euler angles for heading, roll, pitch (all in degrees).
        heading, roll, pitch = sensor.read_euler()
        AccelX, AccelY, AccelZ = sensor.read_linear_acceleration()
        temperature = (sensor.read_temp() * 2) +32
        print(temperature)

        # Print everything out.
        #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(heading, roll, pitch, sys, gyro, accel, mag))

        # Play the sound
        play_sound(float(heading), float(roll), float(pitch), float(AccelX), float(AccelY), float(AccelZ))

    # Delay for a short time
    time.sleep(0)

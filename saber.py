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

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = sensor.get_revision()
#print('Software version:   {0}'.format(sw))
#print('Bootloader version: {0}'.format(bl))
#print('Accelerometer ID:   0x{0:02X}'.format(accel))
#print('Magnetometer ID:    0x{0:02X}'.format(mag))
#print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))
# Read the Euler angles for heading, roll, pitch (all in degrees).
heading, roll, pitch = sensor.read_euler()
# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
sys, gyro, accel, mag = sensor.get_calibration_status()
# Print everything out.
print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
heading, roll, pitch, sys, gyro, accel, mag))
          
          
          

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
print("pygame started")


# Define the sound function
def play_sound(x, y, z):
    frequency = 250 * (abs(x) + abs(y) + abs(z)) / 30
    duration = 100
    sample_rate = 44100
    num_samples = int(duration * sample_rate / 1000)
    #sample_width = 100
    volume = .75
    print('freq={0:0.2F}\t'.format(frequency))


    sound_data = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        sound_sample = float(volume * 1.0 * math.sin(frequency * t * 2 * math.pi))
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
    #pygame.time.wait(duration * 1.2)
    #sound.stop()


# Define the start/stop function
def start_stop(channel):
    global is_recording
    is_recording = not is_recording
    if is_recording:
        print("Recording started")
    else:
        print("Recording stopped")
        pygame.mixer.stop()

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
        # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
        sys, gyro, accel, mag = sensor.get_calibration_status()
        # Print everything out.
        #print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(heading, roll, pitch, sys, gyro, accel, mag))

        # Play the sound
        play_sound(float(heading), float(roll), float(pitch))

    # Delay for a short time
    time.sleep(.16666)

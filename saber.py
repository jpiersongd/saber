import time
import pygame
import board
import busio
import adafruit_bno055
import RPi.GPIO as GPIO
import os

# Initialize the BNO055 sensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

# Initialize the GPIO pins
START_STOP_PIN = 23
MODE_PIN = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(START_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(MODE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the audio
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Define the sound function
def play_sound(x, y, z):
    frequency = 100 + 900 * (abs(x) + abs(y) + abs(z)) / 30
    duration = 100
    sample_rate = 44100
    num_samples = int(duration * sample_rate / 1000)
    sample_width = 2
    volume = 1.0

    sound_data = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        sound_sample = int(volume * 32767.0 * math.sin(frequency * t * 2 * math.pi))
        sound_data.append(sound_sample)
        sound_data.append(sound_sample)

    sound_array = pygame.sndarray.make_sound(sound_data)
    sound_array.play(-1)

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
is_recording = False
while True:
    if is_recording:
        # Read the sensor data
        x, y, z = sensor.acceleration

        # Play the sound
        play_sound(x, y, z)

    # Delay for a short time
    time.sleep(0.1)

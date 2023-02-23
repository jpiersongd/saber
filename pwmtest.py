import RPi.GPIO as GPIO
import time

piezo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(piezo_pin, GPIO.OUT)
piezo_pwm = GPIO.PWM(piezo_pin, 1440)

piezo_pwm.start(20)

while True:
    piezo_pwm.ChangeFrequency(1440)
    time.sleep(0.5)

piezo_pwm.stop()
GPIO.cleanup()

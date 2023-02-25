# saber
These scripts are part of a project to experiment with sound and motion. I wanted to produce a device that would sound a bit like a light saber when swung. 
* saber.wav and sun.wav are example sounds that I wanted to replicate
* analyzer.py takes in a wav file and produces a spectrum anaysis of the frequencies used
* soundonly.py creates the basic sound without any modifications
* saber.py tempers the base sound based on motion measured by an Adafruit BNO055
* pwmtest.py creates a tone on the buzzer pin 18





## Setup notes:
* Runs on Python 3.7 or later.  
* To get the latest version of Python on Raspberry Pi, I found it easiest to download the newest raspbian OS first.
* These all work great on python 3.9 and 64bit Rasbian
* Install the libraries first before running the scripts
  * Sudo pip3 install for each of these
    * numpy
    * pygame
    * adafruit_bno055
    * busio
* audio output is via the audio jack. Be sure to set it to jack and not hdmi




## Hardware setup
| BNO055 Pin | Raspberry Pi Pin |
| --- | --- |
| VIN | 3.3V |
| GND | GND |
| SCL | GPIO3 (SCL) |
| SDA | GPIO2 (SDA) |
| INT | GPIO14 | 



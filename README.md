# saber
These scripts are part of a project to experiment with sound and motion
* analyzer takes in a wav file and produces a spectrum anaysis of the frequencies used in the wav
* soundonly creates the basic sound without any modifications
* saberx recreates a sound that is tempored by the motion of the device
* pwmtest creates a tone on the buzzer pin 18





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

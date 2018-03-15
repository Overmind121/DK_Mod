# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure min and max servo pulse lengths
#this is the bit resolution goes from 0 - 4095
servo_min = 229  # Min pulse length out of 4095
#1100 us
servo_middle = 310  # Max pulse length out of 4095
#1500 us
servo_max = 395  # Max pulse length out of 4095
#1900 us
#multiply by 4.8 to get the microseconds pulse width

'''
so here is how it goes
if you set the pulse to 4095 you will see this on your oscope
__________________________   ____________________
                          |_|

example freq is 50 hz so period the time the signal repeats (1/T =f)
is 0.02seconds
so that means 0.02 seconds or  20ms

measurement I made
    this is close to 1500us (measuring 310 = 1.490ms)
    ratio looks closer to 4.8 > 1490/310 = 4.8
    roughly 150 = 720 microseconds 4.8
    this is close to 1500us (measuring 310 = 1.490ms)
    ratio looks closer to 4.8 > 1490/310 = 4.8
'''


# Set frequency to 60hz, good for servos. measured = 63.21hz
#pwm.set_pwm_freq(60)

pwm.set_pwm_freq(48)
#with my oscope i measure setting 48 in here
#to be closer to 50hz in real measurement (50.76hz)
#measured coming from receiver on donkeycar = 50hz

#every 60 times per second
#____________||___ duration of pulse will always be ~ 15.82ms repeating
#set motors off
pwm.set_pwm(1, 0, 310)
print('Moving servo on channel 0, press Ctrl-C to quit...')
time.sleep(1)
pwm.set_pwm(1, 0, 340)
time.sleep(2)
pwm.set_pwm(1, 0, 310)
time.sleep(1)
    # Move servo on channel O between extremes.
while(1):

    
    
    pwm.set_pwm(0, 0, 310)
    time.sleep(2)

    pwm.set_pwm(0, 0, 530)
    time.sleep(2)

    pwm.set_pwm(0, 0, 310)
    time.sleep(2)

    pwm.set_pwm(0, 0, 130)
    time.sleep(2)

    break;

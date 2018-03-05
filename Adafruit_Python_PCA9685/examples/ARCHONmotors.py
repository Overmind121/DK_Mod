# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
pwm = Adafruit_PCA9685.PCA9685()
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

#Pulse values for drive motor
#where mid will be motor off and maxpoint will by max speed

DRIVE_CHANNEL = 1

MIDPOINT_DRIVE = 225
MAXPOINT_DRIVE = 600
MINPOINT_DRIVE = 150

#Pulse values for servo
#servo will control steering
#where mid will be going straight
STEERING_CHANNEL = 0

MIDPOINT_SERVO = 225
MAXPOINT_SERVO = 600
MINPOINT_SERVO = 150
#600-150 = 450
#450/2 = 225

#does math to find pulse value
def set_servo_pulse(channel, pulse):
  pulse_length = 1000000    # 1,000,000 us per second
  pulse_length //= 60       # 60 Hz
  #print('{0}us per period'.format(pulse_length))
  pulse_length //= 4096     # 12 bits of resolution
  #print('{0}us per bit'.format(pulse_length))
  pulse *= 1000
  pulse //= pulse_length
  #set the frequency to generate pulse

  pwm.set_pwm(channel, 0, pulse)

############################################
#this how we check that we dont pass the maximum values
def clamp(checkVal, minVal ,maxVal):
  if checkVal > maxVal:
    return maxVal
  elif checkVal < minVal:
    return minVal
  else:
    return checkVal


##########################################
'''
These functions control drive motor
'''
##########################################
#we want this function to pass in the speed we want going from 0 all the to 100
def moveForward(speed):
  #we want set pulse to go from 225 - 600 = 375
  set_pulse = int(speed*3.75+MIDPOINT_DRIVE)
  #make sure the set pulse value is within the max and min
  #3.75 = 375 /100 which is max speed
  set_servo_pulse(DRIVE_CHANNEL,set_pulse)

def moveBackward(speed):
  #we want set pulse to go from 225 - 600 = 375
  set_pulse = int(MIDPOINT_DRIVE - speed*3.75)
  #3.75 = 375 /100 which is max speed
  set_servo_pulse(DRIVE_CHANNEL,set_pulse)

def moveStop():
  set_pulse = MIDPOINT_DRIVE
  set_servo_pulse(DRIVE_CHANNEL,set_pulse)

##########################################
'''
These functions control steering servo
'''
##########################################
#we want this function to pass in the angle from 0 - 90 degrees
def turnLeft(angle):
  #we want set pulse to go from 225 - 600 = 375
  set_pulse = int(angle*4.17+MIDPOINT_SERVO)
  set_pulse = clamp(set_pulse,MIDPOINT_SERVO,MAXPOINT_DRIVE)

  #3.75 = 375 /100 which is max speed
  set_servo_pulse(STEERING_CHANNEL,set_pulse)

def turnRight(angle):
  #we want set pulse to go from 225 - 600 = 375
  set_pulse = int(MIDPOINT_SERVO - angle*4.17)
  #3.75 = 375 /100 which is max speed
  set_servo_pulse(STEERING_CHANNEL,set_pulse)

def turnCenter():
  set_pulse = MIDPOINT_SERVO
  set_servo_pulse(STEERING_CHANNEL,set_pulse)

  

  

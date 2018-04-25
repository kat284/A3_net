# ~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 3 Python Script
# File name:                Led File (led.py)
# Description:              Script containing the setup and running of the led portion of the server
# Inputs/Resources:
# Output/Created files:     Led Responses
# Written by:               Team 6
# Created:                  04/23/2018
# Last modified:            04/23/2018
# Version:                  1.0.0
# Example usage:            python3 led.py
# Notes:                    N/A
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3

import RPi.GPIO as GPIO
from led_pin import *
from flask import Flask
from zeroconf import ServiceBrowser, Zeroconf
import time


# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    GPIO.setmode(led_pins['mode'])
    GPIO.setup(led_pins['red'], GPIO.OUT)
    GPIO.setup(led_pins['green'], GPIO.OUT)
    GPIO.setup(led_pins['blue'], GPIO.OUT)
    pin_red = GPIO.PWM(led_pins['red'], 100)
    pin_green = GPIO.PWM(led_pins['green'], 100)
    pin_blue = GPIO.PWM(led_pins['blue'], 100)
    try:
        #Connect to Server
        print("NULL")
    except:
        print("[ERROR] Failed to connect")
        GPIO.cleanup()
        exit(1)
    pin_red.start(0)
    pin_green.start(0)
    pin_blue.start(0)
    intensity = [0,0,0,0,0,0]
    rate = 0.0
    state = 0
    try:
        while 1:
            #if new message Get Argcuments - Set Values
            for itr in range(0,3):
                if state == 1:
                    if intensity[itr] < intensity[itr+3]:
                        intensity[itr] = intensity[itr] + 1.0;
                        if intensity[itr] > intensity[itr+3]:
                            intensity[itr] = intensity[itr+3]
                    elif intensity[itr] > intensity[itr+3]:
                        intensity[itr] = intensity[itr]- 1.0;
                        if intensity[itr] < intensity[itr+3]:
                            intensity[itr] = intensity[itr+3]
                else:
                    if intensity[itr] > 0.0:
                        intensity[itr] = intensity[itr] - 1.0;
                        if intensity[itr] < 0.0:
                            intensity[itr] = 0.0
            pin_red.ChangeDutyCycle(intensity[0] )
            pin_green.ChangeDutyCycle(intensity[1] )
            pin_blue.ChangeDutyCycle(intensity[2] )
            time.sleep(rate)
    except:
        print("[ERROR] Connection Error or Ctrl+C")
        GPIO.cleanup()
        exit(1)

# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

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

from flask import Flask, jsonify, make_response, request, abort
import requests
from zeroconf import ServiceInfo, Zeroconf
import logging
import socket
import sys
from time import sleep
from subprocess import Popen, PIPE
from multiprocessing import Process, Value

cmd = "ip addr list wlan0 |grep 'inet ' |cut -d' ' -f6|cut -d/ -f1"
host = Popen(cmd, shell=True, stdout=PIPE).stdout.read()
host = bytes.decode(host).rstrip()

app = Flask(__name__)

stats = {
        'red': 0.0,
        'green': 0.0,
        'blue': 0.0,
        'rate': 0.0,
        'state': 0
        }
        
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/led', methods=['GET','POST'])
def stats():
    global stats
    if request.method == 'POST':
        request = request.json()
        if request.get("red") != None:
            stats["red"] = request.get("red")
        if request.get("green") != None:
            stats["green"] = request.get("green")
        if request.get("blue") != None:
            stats["blue"] = request.get("blue")
        if request.get("rate") != None:
            stats["rate"] = request.get("rate")
        if request.get("state") != None:
            stats["state"] = request.get("state")
    else:
        return jsonify({'Stats': stats})
   
def loop(): 
    stats = {
        'red': 0.0,
        'green': 0.0,
        'blue': 0.0,
        'rate': 0.0,
        'state': 0
        }
    GPIO.setwarnings(False) 
    GPIO.setmode(led_pins['mode'])
    GPIO.setup(led_pins['red'], GPIO.OUT)
    GPIO.setup(led_pins['green'], GPIO.OUT)
    GPIO.setup(led_pins['blue'], GPIO.OUT)
    pin_red = GPIO.PWM(led_pins['red'], 100)
    pin_green = GPIO.PWM(led_pins['green'], 100)
    pin_blue = GPIO.PWM(led_pins['blue'], 100)
    pin_red.start(0)
    pin_green.start(0)
    pin_blue.start(0)
    intensity = [0,0,0,0,0,0]
    rate = 0.0
    state = 0
    loop = 1
    while loop:
        try:
            intensity[3] =stats["red"]
            intensity[4] =stats["green"]
            intensity[5] =stats["blue"]
            rate = stats["rate"]
            state = stats["state"]
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
        except KeyboardInterrupt:
            GPIO.cleanup()
            loop = 0
            pass
            
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':  
    desc = {'path': '/~team6_led/'}

    info = ServiceInfo("_http._tcp.local.", "LED_API_TEAM6._http._tcp.local.", socket.inet_aton(host), 8003, 0,
                       0, desc, "LED_API.local.")

    zeroconf = Zeroconf()
    print("\nSetting up LED API, press Ctrl-C to exit...\n")
    zeroconf.register_service(info)
    try:
        process = Process(target=loop)
        process.start()
        app.run(host='0.0.0.0', port=8003, debug=True)
        process.join()
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()

# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

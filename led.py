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
        'rate': 1.0,
        'state': 0
        }
        
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)



@app.route('/led', methods=['GET','POST'])
def process_led():
    global stats
    if request.method == 'POST':
		if not request.json:
			abort(400)
        r = request.json
        if r.get("red") != None:
            stats["red"] = float(r.get("red"))
        if r.get("green") != None:
            stats["green"] = float(r.get("green"))
        if r.get("blue") != None:
            stats["blue"] = float(r.get("blue"))
        if r.get("rate") != None:
            stats["rate"] = float(r.get("rate"))
        if r.get("state") != None:
            stats["state"] = int(r.get("state"))
        loop()
        return jsonify({'Stats': stats})
    else:
        return jsonify({'Stats': stats})
   
def loop(): 
    global stats
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
    intensity = [0.0,0.0,0.0,0.0,0.0,0.0]
    loop = 1
    try:
        intensity[3] =stats["red"]
        intensity[4] =stats["green"]
        intensity[5] =stats["blue"]
        rate = stats["rate"]
        state = stats["state"]
        print("apple")
        while loop == 1:
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
            if((state == 1) and (intensity[0] == intensity[3]) and (intensity[1] == intensity[4]) and (intensity[2] == intensity[5])) or ((state == 0) and (intensity[0] == 0) and (intensity[1] == 0) and (intensity[2] == 0)):
                loop = 0
            else:
                time.sleep(rate)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit(1)
    finally:
        GPIO.cleanup()
            
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
        app.run(host='0.0.0.0', port=8003, debug=True)
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

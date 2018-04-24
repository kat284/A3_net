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

#import RPi.GPIO as GPIO
import bluetooth
import sys
import pika
from led_pin import *
from flask import Flask
from zeroconf import ServiceBrowser, Zeroconf


# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class MyListener:

"""
def callback(ch, method, properties, body):
    body = str(body, 'utf-8')
    if body == "red":
        p = GPIO.PWM(channel, frequency)
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
    elif body == "blue":
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
    elif body == "purple":
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
    elif body == "yellow":
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
    elif body == "green":
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
    print("[Checkpoint] Flashing LED to {0}".format(body))
"""

# ~~[Functions]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':

    #app.run(host='0.0.0.0', port=9999, debug=True)
"""""
    GPIO.setmode(led_pins['mode'])
    GPIO.setup(led_pins['red'], GPIO.OUT)
    GPIO.setup(led_pins['green'], GPIO.OUT)
    GPIO.setup(led_pins['blue'], GPIO.OUT)
    pin_red = GPIO.PWM(led_pins['red'], 50)
    pin_green = GPIO.PWM(led_pins['green'], 50)
    pin_blue = GPIO.PWM(led_pins['blue'], 50)

        

    try:
        connection = 0
        credentials = pika.PlainCredentials(username=rmq_params.get("username"), password=rmq_params.get("password"))
        parameters = pika.ConnectionParameters(host=RMQ_IP, virtual_host=rmq_params.get("vhost"),
                                               credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
    except:
        print("[ERROR] Unable to connect to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(
            rmq_params.get("vhost"), RMQ_IP, rmq_params.get("username")))
        print("[ERROR] Verify that vhost is up, credentials are correct or the vhost name is correct!")
        print("[ERROR] Connection closing")
        if connection:
            connection.close()
        GPIO.cleanup()
        exit(1)
    print("[Checkpoint] Connected to vhost '{0}' on RMQ server at '{1}' as user '{2}'".format(rmq_params.get("vhost"),
                                                                                              RMQ_IP, rmq_params.get(
            "username")))
    
    
    
    try:
        channel.queue_bind(exchange=rmq_params.get("exchange"), queue=rmq_params.get("led_queue"),
                           routing_key=rmq_params.get("led_queue"))
        channel.basic_consume(callback, queue=rmq_params.get("led_queue"), no_ack=True)
        print("[Checkpoint] Consuming from RMQ queue: {0}".format(rmq_params.get("led_queue")))
        channel.start_consuming()
    except:
        print("[ERROR] The queue ({0}) was not found or the led.py process was killed".format(
            rmq_params.get("led_queue")))
        print("[ERROR] Verify that the queue is up! You may have to restart the server")
        print("[ERROR] Connection closing")
        connection.close()
        GPIO.cleanup()
        exit(1)
    """
    # ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

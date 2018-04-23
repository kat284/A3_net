#~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 2 Python Script
# File name:                Server File (server.py)
# Description:              Script containing the setup and running of the server
# Inputs/Resources:
# Output/Created files:     Server Side Responses
# Written by:               Team 6
# Created:                  04/02/2018
# Last modified:            04/02/2018
# Version:                  1.0.0
# Example usage:            python3 server.py
# Notes:                    N/A
#~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3

import socket
import sys
import pickle
import os
from cryptography.fernet import Fernet
import
import hashlib

#Server Command:

#~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000
SOCKET_SIZE = 1024
BACKLOG_SIZE= 5
SERVER = None

#~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def loadOptions(argv):
    global SERVER_PORT
    global SOCKET_SIZE
    global BACKLOG_SIZE
    options = {}
    while argv:
        if argv[0][0] == '-':
            options[argv[0]] = argv[1]
        argv = argv[1:]
    if (len(options) == 3) and ('-p' in options) and ('-b' in options) and ('-z' in options):
        SERVER_PORT = options['-p']
        BACKLOG_SIZE = options['-b']
        SOCKET_SIZE = options['-z']
    else:
        return 1
    return 0

if __name__ == '__main__':
    if loadOptions(sys.argv):
        print('[ERROR] Arguments missing or are incorrect')
        print('[ERROR] Server CLOSING')
        sys.exit(1)
    wfa_client = wolframalpha.Client(wolfram_alpha_appid)
    try:
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        SERVER.bind((SERVER_IP,int(SERVER_PORT)))
        print('[Checkpoint] Created socket at ', SERVER_IP, ' on port ', SERVER_PORT)
        SERVER.listen(int(BACKLOG_SIZE))
    except socket.error as error_message:
        if SERVER :
            SERVER.close()
        print("[ERROR] Unable to open the socket: " + str(error_message))
        print('[ERROR] Server CLOSING')
        sys.exit(1)
    while 1:
        print('[Checkpoint] Listening for client connections')
        client, address = SERVER.accept()
        print('[Checkpoint] Accepted client connection from ', SERVER_IP, ' on port ', SERVER_PORT)
        data = client.recv(int(SOCKET_SIZE))
        print('[Checkpoint] Received data: ', data)
        if data:
            message_receive = pickle.loads(data)
            if hashlib.md5(message_receive[1]).hexdigest() != message_receive[2]:
                print('[ERROR] Checksum is NOT VALID')
                print('[ERROR] Server CLOSING')
                sys.exit(1)
            else:
                print('[Checkpoint] Checksum is VALID')
                text_msg = Fernet(message_receive[0]).decrypt(message_receive[1])
                print('[Checkpoint] Decrypt: Using Key: ', message_receive[0], ' | Plaintext: ', text_msg)
                text_msg = text_msg.decode("utf-8")
                cmd = 'espeak "{0}" 2>/dev/null'.format(text_msg)
                os.system(cmd)
                print('[Checkpoint] Speaking: ', text_msg)
                print('[Checkpoint] Sending question to Wolframalpha: ', text_msg)
                res = wfa_client.query(text_msg)
                answer = next(res.results).text
                text_msg = str(answer)
                print('[Checkpoint] Received question from Wolframalpha: ', text_msg)
                en_msg = Fernet(message_receive[0]).encrypt(text_msg.encode('utf-8'))
                print('[Checkpoint] Encrypt: Generated Key: ', message_receive[0], ' | Ciphertext: ', en_msg)
                check_msg = hashlib.md5(en_msg).hexdigest()
                print('[Checkpoint] Generated MD5 Checksum: ', check_msg)
                message_send = (en_msg, check_msg)
                pickle_msg = pickle.dumps(message_send)
                print('[Checkpoint] Sending data: ', pickle_msg)
                client.send(pickle_msg)
        else:
            print('[ERROR] Unknown packet received')
        client.close()

#~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
#~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
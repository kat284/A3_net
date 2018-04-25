# ~~[Start File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# File type:                ECE 4564 Assignment 3 Python Script
# File name:                Server File (server.py)
# Description:              Script containing the setup and running of the server
# Inputs/Resources:
# Output/Created files:     Server Side Responses
# Written by:               Team 6
# Created:                  04/23/2018
# Last modified:            04/23/2018
# Version:                  1.0.0
# Example usage:            python3 server.py
# Notes:                    N/A //https://community.canvaslms.com/docs/DOC-10797-421441247
# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3

from canvas_token import *
import requests
import urllib
import json
"""from menu import *
import bluetooth
from bluetooth import *
import pika"""


# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from flask import Flask, request, jsonify, make_response, send_file
import pymongo
import requests
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth


client = MongoClient('localhost', 27017)

app = Flask(__name__)

auth = HTTPBasicAuth()

db = client['test_database']
    
@auth.get_password
def get_password(username):
    info = {"user": username}
    r = db.posts.find_one(info)
    if r:
        return (r.get("pwd"))
    else:
        return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/cake')
@auth.login_required
def index():
    return 'Hello'

@app.route("/led", methods=['POST', 'GET'])
@auth.login_required
def led():
    if request.method == 'POST':
        print("Good")
    else:
        r = requests.get("http://127.0.0.1:5000/led")

@app.route("/canvas", methods=['GET'])
@auth.login_required
def canvas_ori():
    groupID = "45110000000052698"
    url = "https://canvas.instructure.com/api/v1/groups/" + groupID + "/files/"
    raw_token = "Bearer " + canvas_token
    session = requests.Session()
    session.headers = {'Authorization': raw_token}
    req = session.get(url)
    req = req.json()
    for item in req:
        print(item['filename'])
    return req.json()

@app.route("/canvas/download", methods=['GET'])
@auth.login_required
def canvas_download():
    downloading_file = request.form.get("file")
    groupID = "45110000000052698"
    url = "https://canvas.instructure.com/api/v1/groups/" + groupID + "/files/"
    raw_token = "Bearer " + canvas_token
    session = requests.Session()
    session.headers = {'Authorization': raw_token}
    payload = {'name':  downloading_file}
    req = session.get(url)
    req = req.json()
    id = ""
    for item in req:
        if item['filename'] ==  downloading_file:
            id = str(item['id'])
            break
    req = session.get(url + id)
    req = req.json()
    req = requests.get(req['url'], stream=True)
    with open(downloading_file , 'wb') as dl_file:
        for chunk in req.iter_content():
            dl_file.write(chunk)

    return send_file(downloading_file,
                     attachment_filename=downloading_file,
                     as_attachment=True)

@app.route("/canvas/upload", methods=['POST'])
@auth.login_required
def canvas_upload():
    uploaded_file = request.form.get("file")  
    up_file=open(uploaded_file, 'rb')
    data = up_file.read()
    groupID = "45110000000052698"
    url = "https://canvas.instructure.com/api/v1/groups/" + groupID + "/files/"
    raw_token = "Bearer " + canvas_token
    session = requests.Session()
    session.headers = {'Authorization': raw_token}
    payload = {'name': uploaded_file}
    req = session.post(url, data=payload)
    req = req.json()
    items = req['upload_params'].items()
    upload_url = req['upload_url']
    payload = list(items)
    payload.append(tuple((u'file', data)))
    req = requests.post(upload_url, files=payload)
    return req

@app.route("/custom", methods=['POST', 'GET'])
@auth.login_required
def custom():
    if request.method == 'POST':
        r = requests.post("http://127.0.0.1:5000/custom")
    else:
        r = requests.get("http://127.0.0.1:5000/custom")
        
        
"""
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000, debug=True)

    """  req = session.get(url+id)
        req = req.json()
        req = requests.get(req['url'], stream=True)
        with open(filename, 'wb') as file:
            for chunk in req.iter_content():
                file.write(chunk)
    """

# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

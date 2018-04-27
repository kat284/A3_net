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
#    curl -X GET -u 16:qwe http://172.29.28.14:8000/tasks
#    curl -X POST -u 16:qwe -H "Content-Type: application/json" -d '{"d":"f"}' http://172.29.28.14:8000/tasks

# ~~[Information]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# !/usr/bin/env python3


from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """
import socket
import sys

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from flask import Flask, request, jsonify, make_response, send_file, abort, url_for, send_from_directory
import pymongo
import requests
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth
import os
from werkzeug.utils import secure_filename
from canvas_token import *
import urllib
import json

# ~~[Preprocessor Directives]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

address1 = None
port1 = None

address2 = None
port2 = None

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


@app.route("/canvas", methods=['GET'])
@auth.login_required
def canvas_ori():
    groupID = "45110000000052698"
    url = "https://canvas.instructure.com/api/v1/groups/" + groupID + "/files"
    raw_token = "Bearer " + canvas_token
    session = requests.Session()
    session.headers = {'Authorization': raw_token}
    req = session.get(url)
    req = req.json()
    payload = {}
    num = 0
    for item in req:
        num = num + 1
        payload["file"+str(num)] = item['filename']
    return json.dumps(payload) + "\n"


@app.route("/canvas/download", methods=['GET'])
@auth.login_required
def canvas_download():
    downloading_file = request.form.get("file")
    groupID = "45110000000052698"
    url = "https://canvas.instructure.com/api/v1/groups/" + groupID + "/files/"
    raw_token = "Bearer " + canvas_token
    session = requests.Session()
    session.headers = {'Authorization': raw_token}
    payload = {'name': downloading_file}
    req = session.get(url)
    req = req.json()
    id = ""
    for item in req:
        if item['filename'] == downloading_file:
            id = str(item['id'])
            break
    req = session.get(url + id)
    req = req.json()
    req = requests.get(req['url'], stream=True)
    with open(downloading_file, 'wb') as dl_file:
        for chunk in req.iter_content():
            dl_file.write(chunk)

    return send_file(downloading_file,
                     attachment_filename=downloading_file,
                     as_attachment=True)


app.config['UPLOAD_FOLDER'] = '/home/pi/Desktop'

@app.route("/canvas/upload", methods=['POST'])
@auth.login_required
def canvas_upload():
    uploaded_file = request.files['file']
    name = uploaded_file.filename
    if 'file' not in request.files:
        abort(400)
    
    if name == '':
        abort(400)
    name = secure_filename(name)
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'],name))
    up_file_1 = send_from_directory(app.config['UPLOAD_FOLDER'],name)	
    up_file = open('/home/pi/Desktop/'+name, 'rb')
    data = up_file.read()
    groupID = "45110000000052698"
    url = "https://canvas.instructure.com/api/v1/groups/" + groupID + "/files/"
    raw_token = "Bearer " + canvas_token
    session = requests.Session()
    session.headers = {'Authorization': raw_token}
    payload = {'name': name}
    req = session.post(url, data=payload)
    req = req.json()
    items = req['upload_params'].items()
    upload_url = req['upload_url']
    payload = list(items)
    payload.append(tuple((u'file', data)))
    req = requests.post(upload_url, files=payload)
    return "\n"

@app.route('/calculate/<int:val1>/<int:val2>', methods=['GET'])
@auth.login_required
def get_result(val1, val2):
    global address1
    global port1
    if (address1 == None or port1 == None):
        abort(400)
    customurl = 'http://{}:{}/calculate/'.format(address1, port1) + str(val1) +'/' + str(val2)
    r = requests.get(customurl)
    return r.text


@app.route('/value/<int:val>', methods=['POST'])
@auth.login_required
def post_val(val):
    global address1
    global port1
    if (address1 == None or port1 == None):
        abort(400)
    customurl = 'http://{}:{}/value/'.format(address1, port1) + str(val)
    val = request.args.get('firstnumber')
    print(val)
    r = requests.post(customurl)
    return "\n"
    
@app.route('/tasks', methods=['POST','GET'])
@auth.login_required
def tasks():
    global address1, address2, port1, port2
    if (address1 == None or port1 == None):
        abort(400)
    customurl = 'http://{}:{}/tasks'.format(address1, port1)
    if request.method == 'POST':
        payload = request.json
        r = requests.post(customurl,json=payload)
        return "\n"
    else:
        r = requests.get(customurl)
        return r.text

@app.route("/led", methods=['POST', 'GET'])
@auth.login_required
def led():
    global address2
    global port2
    if (address2 == None or port2 == None):
            abort(400)
    payload = {}
    customurl = 'http://{}:{}/led'.format(address2, port2)
    if request.method == 'POST':
        if not request.json:
            abort(400)
        r = request.json
        if r.get("red") != None:
            payload["red"] = r.get("red")
        if r.get("green") != None:
            payload["green"] = rr.get("green")
        if r.get("blue") != None:
            payload["blue"] = r.get("blue")
        if r.get("rate") != None:
            payload["rate"] = r.get("rate")
        if r.get("state") != None:
            payload["state"] = r.get("state")
        r = requests.post(customurl,json=payload)
        return "\nDone\n"
    else:
        r = requests.get(customurl)
        return r.text 

def on_service_state_change(zeroconf, service_type, name, state_change):
    global address1, address2, port1, port2

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            if info.server == 'CUSTOM_API.local.':
                print('\n')
                print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
                found = True
                address1 = socket.inet_ntoa(info.address)
                port1 = info.port
                print("Saved Address & Port for CUSTOM_API")
                print("\n")
            elif info.server == 'LED_API.local.':
                print('\n')
                print("Service %s of type %s state changed: %s" % (name, service_type, state_change))
                found = True
                address2 = socket.inet_ntoa(info.address)
                port2 = info.port
                print("Saved Address & Port for LED_API")
                print('\n')

# ~~[Variables]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

if __name__ == '__main__':
    zeroconf = Zeroconf()
    print("\nSetting up Server, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])

    try:
        app.run(host='0.0.0.0', port=8000, debug=True)
    except KeyboardInterrupt:
       pass 
    finally:
        zeroconf.close()

# ~~[Core]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#      .--.      .'-.      .--.      .--.      .--.      .-'.      .--. #
#::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/::::::::'/:::::#
# `--'      `-.'      `--'      `--'      `--'      `--'      `.-'      #
# ~~[End File]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """
import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

from flask import Flask, request, jsonify, make_response, send_file
import pymongo
import requests
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth

address1 = None
port1 = None

address2 = None
port2 = None

client = MongoClient('localhost', 27017)

app = Flask(__name__)

auth = HTTPBasicAuth()

db = client['test_database']


if __name__ == '__main__':


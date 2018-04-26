from flask import Flask, jsonify, make_response, request, abort
import requests
from zeroconf import ServiceInfo, Zeroconf
import logging
import socket
import sys
from time import sleep
from subprocess import Popen, PIPE

cmd = "ip addr list wlan0 |grep 'inet ' |cut -d' ' -f6|cut -d/ -f1"
host = Popen(cmd, shell=True, stdout=PIPE).stdout.read()
host = bytes.decode(host).rstrip()

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/calculate/<int:val1>/<int:val2>', methods=['GET'])
def get_result(val1, val2):
    return jsonify({'result': str(val1 * val2)})


#
@app.route('/value', methods=['POST'])
def post_val():
    val = request.args.get('firstnumber')
    return str(val)


#
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


if __name__ == '__main__':

    desc = {'path': '/~team6_custom/'}

    info = ServiceInfo("_http._tcp.local.", "CUSTOM_TEAM6._http._tcp.local.", socket.inet_aton(host), 5000, 0,
                       0, desc, "CUSTOM.local.")

    zeroconf = Zeroconf()
    print("\nSetting up Custom API, press Ctrl-C or Ctrl-Z to exit...\n")
    zeroconf.register_service(info)
    try:
        while True:
            app.run(host='0.0.0.0', port=8001, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.unregister_service(info)
        zeroconf.close()





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


@app.route('/calculate/<str:val1>/<str:val2>', methods=['GET'])
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


#################################################################
@app.route('/todo/api/v1.0/tasks2', methods=['GET'])
def get_tasks2():
    return jsonify({'tasks': tasks})


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    desc = {'path': '/~paulsm/'}

    info = ServiceInfo("_http._tcp.local.", "Paul's Test Web Site._http._tcp.local.", socket.inet_aton(host), 5000, 0,
                       0, desc, "team6_api.local.")

    zeroconf = Zeroconf()
    print("Registration of a service, press Ctrl-C to exit...")
    zeroconf.register_service(info)
    try:
        while True:
            # sleep(0.1)
            # app.run(debug=True)
            app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()





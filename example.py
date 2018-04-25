from __future__ import absolute_import, division, print_function, unicode_literals

""" Example of browsing for a service (in this case, HTTP) """
import requests
import logging
import socket
import sys
from time import sleep

from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf

address1 = None
port1 = None

address2 = None
port2 = None


def on_service_state_change(zeroconf, service_type, name, state_change):
    global address1, address2, port1, port2

    found = False

    print("Service %s of type %s state changed: %s" % (name, service_type, state_change))

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        # if info:
        if info:
            print("  Address: %s:%d" % (socket.inet_ntoa(info.address), info.port))
            print("  Weight: %d, priority: %d" % (info.weight, info.priority))

            print("  Server: %s" % (info.server,))
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print("    %s: %s" % (key, value))
            else:
                print("  No properties")

            if info.server == 'team6_api.local.':
                found = True
                address1 = socket.inet_ntoa(info.address)
                port1 = info.port


        else:
            print("  No info")
        print('\n')


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)

    zeroconf = Zeroconf()
    print("\nBrowsing services, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])

    try:
        while True:
            if address1 and port1:
                break

    except KeyboardInterrupt:
        pass

    finally:
        zeroconf.close()
        print(address1)
        print(port1)

    r = requests.get('http://{}:{}/tasks'.format(address1, port1))
    print(r.text)

    payload = {"title": "read a book"}
    r = requests.post('http://{}:{}/tasks'.format(address1, port1), json=payload)
    print(r.text)

    """
    r=requests.get('http://{}:{}/calculate/2/3'.format(address1,port1))
    print(r.text)



    r=requests.post('http://{}:{}/value/2'.format(address1,port1))
    print(r.text)
    """

"""
payload = {'key1': 'value1', 'key2': 'value2'}
r = requests.post("http://httpbin.org/post", data=payload)
"""

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


if __name__ == '__main__':

    zeroconf = Zeroconf()
    print("\nSetting up Example Server, waiting for CUSTOM_API service...\n")
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change])

    try:
        while True:
            if address1 and port1:
                break
        print("=====================================") 
        print('http://{}:{}/tasks'.format(address1, port1))         
        print("=====================================")  
        r = requests.get('http://{}:{}/tasks'.format(address1, port1))
        print(r.text)
        print("=====================================") 
        print('http://{}:{}/tasks'.format(address1, port1))   
        payload = {"title": "read a book"}
        print("json=",payload)     
        print("=====================================")    
        
        r = requests.post('http://{}:{}/tasks'.format(address1, port1), json=payload)
        print(r.text)
        print("=====================================") 
        print('http://{}:{}/tasks'.format(address1, port1))         
        print("=====================================") 
        r = requests.get('http://{}:{}/tasks'.format(address1, port1))
        print(r.text)
        print("=====================================") 
        print('http://{}:{}/calculate/2/3'.format(address1, port1))         
        print("=====================================")       
        r=requests.get('http://{}:{}/calculate/2/3'.format(address1,port1))
        print(r.text)
        print("=====================================") 
        print('http://{}:{}/value/2'.format(address1, port1))         
        print("=====================================") 
        r=requests.post('http://{}:{}/value/2'.format(address1,port1))
        print(r.text)
        
    except KeyboardInterrupt:
        pass

    finally:
        zeroconf.close()

#!/usr/bin/python3

import os
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="Choose a network interface e.g. eth0")

args = parser.parse_args()

interfaces = {}
userSelection = []
def main():
    list_interfaces()
    while True:
        userInterface = int(input("Choose interface\n"))
        interface = userSelection[userInterface]
        display_interface(interface)
        address = input('Set new IP address')
        netmask = input('Set new subnet')
        interfaces[interface]['address'] = address
        interfaces[interface]['netmask'] = netmask
        set_IP(interface)

def display_interface(interface):
    for k, v in interfaces[interface].items():
        print(str(k) + ' : ' + str(v))

def list_interfaces():
    for _, dir, _ in os.walk('/sys/class/net/'):
        for index, interface in enumerate(dir):
            interfaces[interface] = {}
            get_IP(interface)
            userSelection.append(interface)
            print(str(index) + ') ' + interface)

def get_IP(interface):
     ipSettings = os.popen('ip a show dev ' + interface).read()
     gateway = os.popen('ip r').read()
     get_everything(interface, ipSettings, gateway)

def get_everything(interface, ipSettings, gateway):
    ipMatch = re.search('inet ([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})/', ipSettings)
    if ipMatch is not None:
        interfaces[interface]['address'] = ipMatch.group(1)

    subnetMatch = re.search(r'inet\s.*\/([0-9]{1,3}).*', ipSettings)
    if subnetMatch is not None:
        interfaces[interface]['netmask'] = get_subnet(subnetMatch.group(1))

    stateMatch = re.search(r'state ([D-W]{2,7}) ', ipSettings)
    if stateMatch is not None:
        interfaces[interface]['state'] = stateMatch.group(1)

    gatewayMatch = re.search(r'default\svia\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*', gateway)
    interfaces[interface]['gateway'] = gatewayMatch.group(1)

def get_subnet(cidr):
    octect = int(cidr.strip()) // 8
    remainder = int(cidr.strip()) % 8
    subnet = ['0', '0', '0', '0']
    for i in range(octect):
       subnet[i] = '255'
    if remainder != 0:
        subnet[octect] = str(256 - 2 ** (8 - remainder))
    return '.'.join(subnet)

def set_IP(interface):
    os.popen('sudo ip addr flush dev ' + interface)
    ip = interfaces[interface]['address']
    ip += '/' + interfaces[interface]['netmask']
    os.popen('sudo ip addr add ' + ip + ' dev ' + interface)

if __name__ == '__main__':
    main()

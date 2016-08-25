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
    print(interfaces)

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
    interfaces[interface]['address'] = ipMatch.group(1)

    subnetMatch = re.search(r'inet\s.*\/([0-9]{1,3}).*', ipSettings)
    interfaces[interface]['netmask'] = get_subnet(subnetMatch.group(1))

    stateMatch = re.search(r'state ([D-W]{2,7}) ', ipSettings)
    interfaces[interface]['state'] = stateMatch.group(1)

    gatewayMatch = re.search(r'default\svia\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*', gateway)
    interfaces[interface]['gateway'] = gatewayMatch.group(1)

def get_subnet(cidr):
    octect = int(cidr.strip()) // 8
    remainder = int(cidr.strip()) % 8
    subnet = ['0', '0', '0', '0']
    for i in range(octect):
       subnet[i] = '255'
    subnet[octect] = str(256 - 2 ** (8 - remainder))
    return '.'.join(subnet)

if __name__ == '__main__':
    main()

#!/usr/bin/python3

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="Choose a network interface e.g. eth0")

args = parser.parse_args()

interfaces = {}
def main():
    list_interfaces()
    get_IP('eth0')
    get_cidr('eth0')
    get_subnet('19')

def list_interfaces():
    for _, dir, _ in os.walk('/sys/class/net/'):
        for index, interface in enumerate(dir):
            interfaces[index] = {'interface':interface }
            print(str(index) + ') ' + interface)

def get_IP(interface):
    ip = os.popen("ip a show dev " + interface + " | sed -rn 's/inet\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})\/.*/\\1/p'").read()
    print(str(ip).strip())

def get_cidr(interface):
    cidr = os.popen("ip a show dev " + interface + " | sed -rn 's/inet\s.*\/([0-9]{1,3}).*/\\1/p'").read()

def get_subnet(cidr):
    octect = int(cidr.strip()) // 8
    remainder = int(cidr.strip()) % 8
    subnet = ['0', '0', '0', '0']
    for i in range(octect):
       subnet[i] = '255'
    subnet[octect] = str(256 - 2 ** (8 - remainder))
    print('.'.join(subnet))

if __name__ == '__main__':
    main()

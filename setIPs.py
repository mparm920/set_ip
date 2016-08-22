#!/usr/bin/python3

import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="Choose a network interface e.g. eth0",
                    action="store_true")

args = parser.parse_args()

interfaces = []
def main():
    list_interfaces()

def list_interfaces():
    for _, dir, _ in os.walk('/sys/class/net/'):
        interfaces = dir
        for index, interface in enumerate(dir):
            print(str(index) + ') ' + interface)
    print(interfaces)

if __name__ == '__main__':
    main()

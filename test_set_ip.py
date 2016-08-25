#!/usr/bin/python3

import pytest
import setIPs


def test_get_subnet_24():
    assert setIPs.get_subnet('24') == '255.255.255.0'

def test_get_subnet_19():
    assert setIPs.get_subnet('19') == '255.255.224.0'

def test_get_subnet_1():
    assert setIPs.get_subnet('1') == '128.0.0.0'

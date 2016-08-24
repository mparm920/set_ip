#!/usr/bin/python3

import unittest
import setIPs

class testSetIP(unittest.TestCase):

    def test_get_subnet(self):
        self.assertEqual(setIPs.get_subnet('24'), '255.255.255.0')

    def test_get_subnet_19(self):
        self.assertEqual(setIPs.get_subnet('19'), '255.255.224.0',
                msg='cidr 19 equals 255.255.224.0')
        

if __name__ == '__main__':
    unittest.main()

"""

Unit test to check transform_coords.py functions are behaving as expected.

"""

import unittest
from transform_coords import *

class TestStringMethods(unittest.TestCase):

    def test_check_line(self):
        self.assertEqual(check_line("367478.9\t8131831.3\n"), ("367478.9","8131831.3"))

    def test_check_float(self):
        self.assertEqual(check_float("367478.9","8131831.3"), (float(367478.9), float(8131831.3)))   

    def test_check_grid(self):
        self.assertEqual(check_grid("MGA94", 54), "EPSG:28354")
        self.assertEqual(check_grid("GDA2020", 51), "EPSG:7851")

if __name__ == '__main__':
    unittest.main()
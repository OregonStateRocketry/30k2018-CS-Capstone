import unittest
import time
import apogee

from apogee import apogee_detect

class test_apogee_methods(unittest.TestCase):

    # Test altitude decreasing
    def test_altitude_decrease(self):
        apogee1 = apogee_detect()

        # acceleration isn't at a threshold
        apogee1.check_apogee(0.40, 20000)
        self.assertFalse(apogee1.check_apogee(0.20, 19000))

        # acceleration is at the far threshold
        self.assertFalse(apogee1.check_apogee(0.10, 18000))

        # acceleration is at the close threshold
        self.assertTrue(apogee1.check_apogee(0.10, 17000))

    # Test far threshold timer
    def test_timer_far(self):
        apogee1 = apogee_detect()
        apogee1.check_apogee(0.20, 30000)
        # time isn't up
        self.assertFalse(apogee1.check_apogee(0.40, 30000))

        # time is up
        time.sleep(5)
        self.assertTrue(apogee1.check_apogee(0.40, 30000))

    # Test close threshold timer
    def test_timer_close(self):
        apogee1 = apogee_detect()
        apogee1.check_apogee(0.10, 30000)
        # time isn't up
        self.assertFalse(apogee1.check_apogee(0.40, 30000))

        # time is up
        time.sleep(4)
        self.assertTrue(apogee1.check_apogee(0.40, 30000))

    # Test for missed apogee
    def test_missed(self):
        apogee1 = apogee_detect()
        self.assertFalse(apogee1.check_apogee(0.20, 30000))

        # missed apogee and falling
        self.assertTrue(apogee1.check_apogee(1.1, 20000))

if __name__ == '__main__':
    unittest.main()

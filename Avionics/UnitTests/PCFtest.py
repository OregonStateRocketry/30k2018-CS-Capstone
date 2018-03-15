import unittest
import PCF8523
import time
class TestStringMethods(unittest.TestCase):

    def test_counts(self):
        sensor = PCF8523.PCF8523()
        t1 = sensor.gettime()
        time.sleep(1)
        t2 = sensor.gettime()
        self.assertTrue((time.mktime(t2) - time.mktime(t1) == 1)or(time.mktime(t2) - time.mktime(t1) == 2))

    def test_set(self):
        sensor = PCF8523.PCF8523()
        setter = time.localtime()
        sensor.settime(setter)
        time.sleep(1)
        t2 = sensor.gettime()
        self.assertTrue((time.mktime(t2) - time.mktime(setter) == 1)or(time.mktime(t2) - time.mktime(setter) == 2))

if __name__ == '__main__':
    unittest.main()

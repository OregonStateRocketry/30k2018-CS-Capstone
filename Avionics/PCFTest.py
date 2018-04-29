import unittest
import time, sys, os
import ESCMotor, MPL3115A2, MPU9250, PCF8523, mainPayload, payloadState
import pigpio

class TestPCF8523(unittest.TestCase):
    def test_gettime(self):
        pcf = PCF8523.PCF8523()
        firstTime = pcf.gettime()
        self.assertIsNotNone(firstTime)
        time.sleep(1)
        secondTime = pcf.gettime()
        self.assertTrue(time.mktime(firstTime) < time.mktime(secondTime))

    def test_settime(self):
        pcf = PCF8523.PCF8523()
        setter = time.localtime()
        pcf.settime(setter)
        time.sleep(1)
        t2 = pcf.gettime()
        self.assertTrue((time.mktime(t2) - time.mktime(setter) == 1)or(time.mktime(t2) - time.mktime(setter) == 2))

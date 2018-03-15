import unittest
import MPU6050
import time
import pigpio
class TestStringMethods(unittest.TestCase):

    def test_read(self):
        piggy = pigpio.pi()
        mpuA = MPU6050.MPU6050(pi=piggy, gpio=22)
        for x in range(100):
            m1 = mpuA.read_all()
            assertTrue(m1['gyro_x'] < 1)
            assertTrue(m1['gyro_x'] > -1)
            assertTrue(m1['gyro_y'] < 1)
            assertTrue(m1['gyro_y'] > -1)
            assertTrue(m1['gyro_z'] < 1)
            assertTrue(m1['gyro_z'] > -1)
            assertTrue(m1['acc_x'] > -0.05)
            assertTrue(m1['acc_x'] < 0.05)
            assertTrue(m1['acc_y'] > -0.05)
            assertTrue(m1['acc_y'] < 0.05)
            assertTrue(m1['acc_z'] < 1.2)
            assertTrue(m1['acc_z'] > 0.8)
if __name__ == '__main__':
    unittest.main()

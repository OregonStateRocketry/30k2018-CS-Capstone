import unittest
import MPL3115A2
import time
class TestStringMethods(unittest.TestCase):

    def test_temp(self):
        sensor = MPL3115A2.MPL3115A2()
        sensor.update()
        time.sleep(0.1)
        temp = sensor.temperature()

        self.assertTrue(temp < 50)
        self.assertTrue(temp > 0)

    def test_pres(self):
        sensor = MPL3115A2.MPL3115A2()
        sensor.update()
        time.sleep(0.1)
        pres = sensor.pressure()
        self.assertTrue(pres < 110000)
        self.assertTrue(pres > 90000)

if __name__ == '__main__':
    unittest.main()

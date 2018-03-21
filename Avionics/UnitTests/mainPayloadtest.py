import unittest
import mainPayload
import os.path

class TestStringMethods(unittest.TestCase):

    def test_read(self):
        self.assertFalse(os.path.isfile("av_out.csv"))
        mainPayload.runLoop()
        self.assertTrue(os.path.isfile("av_out.csv"))
if __name__ == '__main__':
    unittest.main()

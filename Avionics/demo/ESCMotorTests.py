import unittest
import ESCMotor

class TestMotorFunctions(unittest.TestCase):

    def test_init(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        self.assertEqual(   m1.Kp, 2.0)
        self.assertEqual(   m1.Ki, 0.0)
        self.assertEqual(   m1.Kd, 1.0)
        self.assertEqual(   m1.set_point, 0.0)
        self.assertEqual(   m1.ESC_MIN, 1000)
        self.assertEqual(   m1.ESC_MAX, 2000)
        self.assertEqual(   m1.PIN, 18)

    def test_set_ESC_range(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        self.assertTrue( m1.set_ESC_range() )
        print("500->? = ", pid_to_pwm(500))

    def test_set_motor(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        self.assertFalse( m1.set_motor(5) )
        self.assertTrue( m1.set_motor(1500) )
        self.assertFalse( m1.set_motor(5000) )

    def test_pid_to_pwm(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        print("pid_to_pwm(500) -> ", pid_to_pwm(500))

    def test_clear(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        self.assertEqual(   m1.PTerm, 0.0)
        self.assertEqual(   m1.ITerm, 0.0)
        self.assertEqual(   m1.DTerm, 0.0)
        self.assertEqual(   m1.last_error, 0.0)
        self.assertEqual(   m1.windup_guard, 20)
        self.assertTrue(    m1.last_time < time.time() )

    def test_pid_to_pwm(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        print("update(1.0) -> ", update(1.0))

    def test_update_motor(self):
        piggy = pigpio.pi()
        m1 = Motor(pi=piggy, pin=18)
        self.assertFalse( m1.set_motor(5) )
        self.assertTrue( m1.set_motor(1500) )
        self.assertFalse( m1.set_motor(5000) )

if __name__ == "__main__":
    unittest.main()

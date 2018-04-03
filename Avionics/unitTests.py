import unittest
import time, sys, os
import ESCMotor, MPL3115A2, MPU9250, PCF8523, mainPayload, payloadState
import pigpio

class TestESCMotor(unittest.TestCase):
    def test_init(self):
        piggy = pigpio.pi()
        m1 = ESCMotor.Motor(pi=piggy, pin=18)
        self.assertEqual(m1.Kp, 2.0)
        self.assertEqual(m1.Ki, 0.0)
        self.assertEqual(m1.Kd, 1.0)
        self.assertEqual(m1.set_point, 0.0)
        self.assertEqual(m1.ESC_MIN, 800)
        self.assertEqual(m1.ESC_MAX, 1800)
        self.assertEqual(m1.PIN, 18)

    # def test_set_ESC_range(self):
    #     piggy = pigpio.pi()
    #     m1 = ESCMotor.Motor(pi=piggy, pin=18)
    #     self.assertTrue(m1.set_ESC_range())

    def test_set_motor(self):
        piggy = pigpio.pi()
        m1 = ESCMotor.Motor(pi=piggy, pin=18)
        self.assertFalse(m1.set_motor(5))
        self.assertTrue(m1.set_motor(1500))
        self.assertFalse(m1.set_motor(5000))

    def test_pid_to_pwm(self):
        piggy = pigpio.pi()
        m1 = ESCMotor.Motor(pi=piggy, pin=18)

    def test_clear(self):
        piggy = pigpio.pi()
        m1 = ESCMotor.Motor(pi=piggy, pin=18)
        self.assertEqual(m1.PTerm, 0.0)
        self.assertEqual(m1.ITerm, 0.0)
        self.assertEqual(m1.DTerm, 0.0)
        self.assertEqual(m1.last_error, 0.0)
        self.assertEqual(m1.windup_guard, 20)
        self.assertTrue(m1.last_time < time.time())

    def test_pid_to_pwm2(self):
        piggy = pigpio.pi()
        m1 = ESCMotor.Motor(pi=piggy, pin=18)

    def test_update_motor(self):
        piggy = pigpio.pi()
        m1 = ESCMotor.Motor(pi=piggy, pin=18)
        self.assertFalse(m1.set_motor(5))
        self.assertTrue(m1.set_motor(900))
        self.assertFalse(m1.set_motor(5000))
        self.assertEqual(m1.update_motor(0.0), (0, 800))


class TestMainPayload(unittest.TestCase):
    def test_read(self):
        os.remove("av_out.csv")
        self.assertFalse(os.path.isfile("av_out.csv"))
        payload = mainPayload.Payload()
        payload.runLoop(5)
        self.assertTrue(os.path.isfile("av_out.csv"))


class TestPCF8523(unittest.TestCase):
    def test_gettime(self):
        pcf = PCF8523.PCF8523()
        firstTime = pcf.gettime()
        self.assertIsNotNone(firstTime)
        secondTime = pcf.gettime()
        # self.assertTrue(firstTime < secondTime)

    def test_settime(self):
        pcf = PCF8523.PCF8523()


class TestPayloadState(unittest.TestCase):
    def test_PreLaunchPhase(self):
        state = payloadState.PreLaunchPhase()
        self.assertEquals(str(state), 'PreLaunchPhase')
        data = {'acc_z': 2}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'PreLaunchPhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'PrimaryEnginePhase')

    def test_PrimaryEnginePhase(self):
        state = payloadState.PrimaryEnginePhase()
        self.assertEquals(str(state), 'PrimaryEnginePhase')
        data = {'acc_z': 1.0}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'PrimaryEnginePhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'SecondaryEnginePhase')

    def test_SecondaryEnginePhase(self):
        state = payloadState.SecondaryEnginePhase()
        data = {'acc_x': 1, 'acc_y': 1, 'acc_z': 1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'SecondaryEnginePhase')
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'SecondaryEnginePhase')
        # Its waiting for the avg acceleration to be low
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'SecondaryEnginePhase')
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'SecondaryEnginePhase')
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'SecondaryEnginePhase')
        # AND for the altitude to decrease
        data['alt'] = data['alt'] - 10
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'ExperimentPhase')

    def test_ExperimentPhase(self):
        state = payloadState.ExperimentPhase()
        data = {'acc_z': 1}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'ExperimentPhase')
        data['acc_z'] = 2
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'DescentPhase')

        # Should also check time.. but 15 sec is sooo long
        state = payloadState.ExperimentPhase()
        data = {'acc_z': 1}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'ExperimentPhase')
        time.sleep(14)
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'ExperimentPhase')
        time.sleep(1)
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'DescentPhase')

    def test_DescentPhase(self):
        state = payloadState.DescentPhase()
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.7}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'DescentPhase')
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'DescentPhase')
        data = {'acc_x': 1, 'acc_y': 1, 'acc_z': 1}
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'DescentPhase')
        time.sleep(5)
        state = state.monitorPhase(data)
        self.assertEquals(str(state), 'FinalPhase')


class TestMPU9250(unittest.TestCase):
    def test_read(self):
        piggy = pigpio.pi()
        mpuA = MPU9250.MPU9250(pi=piggy, gpio=17)
        for x in range(10):
            m1 = mpuA.read_all()
            self.assertTrue(m1['gyro_x'] < 2)
            self.assertTrue(m1['gyro_x'] > -2)
            self.assertTrue(m1['gyro_y'] < 2)
            self.assertTrue(m1['gyro_y'] > -2)
            self.assertTrue(m1['gyro_z'] < 2)
            self.assertTrue(m1['gyro_z'] > -2)
            self.assertTrue(m1['acc_x'] > -0.05)
            self.assertTrue(m1['acc_x'] < 0.05)
            self.assertTrue(m1['acc_y'] > -0.05)
            self.assertTrue(m1['acc_y'] < 0.05)
            self.assertTrue(m1['acc_z'] < 1.2)
            self.assertTrue(m1['acc_z'] > 0.8)

if __name__ == "__main__":
    unittest.main()

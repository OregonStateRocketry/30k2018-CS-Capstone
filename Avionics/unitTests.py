import unittest
import time, sys, os
import ESCMotor, MPL3115A2, MPU9250, PCF8523
import mainPayload, mainRocket, payloadState, rocketState
import pigpio
import csv

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
        os.remove("av_payload.csv")
        self.assertFalse(os.path.isfile("av_payload.csv"))
        payload = mainPayload.Payload()
        payload.runLoop(5)
        self.assertTrue(os.path.isfile("av_payload.csv"))
        with open('av_payload.csv') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            row1str = ','.join(row1)
            self.assertEqual(row1str, "state,time,gyro_x,gyro_y,gyro_z,acc_x,acc_y,acc_z,temp(c),alt(m),acc_pid,acc_pwm,gyro_pid,gyro_pwm")

            row2 = next(reader)
            self.assertEqual(row2[0],'0')
            self.assertTrue(float(row2[1]) <= time.time())
            self.assertTrue(float(row2[1]) > time.time() -2)
            self.assertTrue(float(row2[2]) > -10)
            self.assertTrue(float(row2[2]) < 10)
            self.assertTrue(float(row2[3]) > -10)
            self.assertTrue(float(row2[3]) < 10)
            self.assertTrue(float(row2[4]) > -10)
            self.assertTrue(float(row2[4]) < 10)
            self.assertTrue(float(row2[5]) > -0.5)
            self.assertTrue(float(row2[5]) < 0.5)
            self.assertTrue(float(row2[6]) > -0.5)
            self.assertTrue(float(row2[6]) < 0.5)
            self.assertTrue(float(row2[7]) > 0.5)
            self.assertTrue(float(row2[7]) < 1.5)

class TestMainRocket(unittest.TestCase):
    def test_read(self):
        os.remove("av_rocket.csv")
        self.assertFalse(os.path.isfile("av_rocket.csv"))
        rocket = mainRocket.Rocket()
        rocket.runLoop(5)
        self.assertTrue(os.path.isfile("av_rocket.csv"))
        with open('av_rocket.csv') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            row1str = ','.join(row1)
            self.assertEqual(row1str, "state,time,17_gyro_x,17_gyro_y,17_gyro_z,17_acc_x,17_acc_y,17_acc_z,27_gyro_x,27_gyro_y,27_gyro_z,27_acc_x,27_acc_y,27_acc_z,22_gyro_x,22_gyro_y,22_gyro_z,22_acc_x,22_acc_y,22_acc_z,temp(c),alt(ft)")
            row2 = next(reader)
            self.assertEqual(row2[0],'0')
            self.assertTrue(float(row2[1]) <= time.time())
            self.assertTrue(float(row2[1]) > time.time() -2)
            self.assertTrue(float(row2[2]) > -10)
            self.assertTrue(float(row2[2]) < 10)
            self.assertTrue(float(row2[3]) > -10)
            self.assertTrue(float(row2[3]) < 10)
            self.assertTrue(float(row2[4]) > -10)
            self.assertTrue(float(row2[4]) < 10)
            self.assertTrue(float(row2[5]) > -0.5)
            self.assertTrue(float(row2[5]) < 0.5)
            self.assertTrue(float(row2[6]) > -0.5)
            self.assertTrue(float(row2[6]) < 0.5)
            self.assertTrue(float(row2[7]) > 0.5)
            self.assertTrue(float(row2[7]) < 1.5)

class TestMPL3115A2(unittest.TestCase):
    def test_read(self):
        mpl = MPL3115A2.MPL3115A2()
        num = 10
        t, p = mpl.readTempAlt()
        while num:
            num -=1
            time.sleep(0.1)
            lp = p
            lt = t
            t, p = mpl.readTempAlt()
            #check that noise is small
            self.assertTrue(abs(p-lp) <= 5)
            self.assertTrue(abs(t-lt) <= 2)
            #check that values are in bounds
            self.assertTrue(p < 10000)
            self.assertTrue(t < 50)
            self.assertTrue(t > 0)


class TestPayloadState(unittest.TestCase):
    def test_PreLaunchPhase(self):
        state = payloadState.PreLaunchPhase()
        self.assertEqual(str(state), 'PreLaunchPhase')
        data = {'acc_z': 2}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'PreLaunchPhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'PrimaryEnginePhase')

    def test_PrimaryEnginePhase(self):
        state = payloadState.PrimaryEnginePhase()
        self.assertEqual(str(state), 'PrimaryEnginePhase')
        data = {'acc_z': 1.0}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'PrimaryEnginePhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')

    def test_SecondaryEnginePhase(self):
        state = payloadState.SecondaryEnginePhase()
        data = {'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        data = {'alt': 27122}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase') #setting max alt
        data['alt'] = data['alt'] - 600
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase') #just dropping far enough is not sufficient
        time.sleep(2.05)
        data['alt'] = data['alt'] + 305
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase') #neither is just being below for long Enough
        data['alt'] = data['alt'] - 305
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'ExperimentPhase')


    def test_ExperimentPhase(self):
        state = payloadState.ExperimentPhase()
        data = {'acc_z': 1, 'alt' : 30000}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'ExperimentPhase')
        data['acc_z'] = 2
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')

        # Should also check time.. but 15 sec is sooo long
        state = payloadState.ExperimentPhase()
        data = {'acc_z': 1, 'alt' : 30000}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'ExperimentPhase')
        time.sleep(11)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'ExperimentPhase')
        time.sleep(1)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')

        # test altitude
        state = payloadState.ExperimentPhase()
        data = {'acc_z': 1, 'alt' : 30000}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'ExperimentPhase')
        data['alt'] = 9999
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')

    def test_DescentPhase(self):
        state = payloadState.DescentPhase()
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.7}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')
        data = {'acc_x': 0, 'acc_y': 0, 'acc_z': 1}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')
        time.sleep(5)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'FinalPhase')


class TestRocketState(unittest.TestCase):
    def test_PreLaunchPhase(self):
        state = rocketState.PreLaunchPhase()
        self.assertEqual(str(state), 'PreLaunchPhase')
        data = {'acc_z': 2}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'PreLaunchPhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'PrimaryEnginePhase')

    def test_PrimaryEnginePhase(self):
        state = rocketState.PrimaryEnginePhase()
        self.assertEqual(str(state), 'PrimaryEnginePhase')
        data = {'acc_z': 1.0}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'PrimaryEnginePhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')

    def test_SecondaryEnginePhase(self):
        state = rocketState.SecondaryEnginePhase()
        data = {'acc_x': 1, 'acc_y': 1, 'acc_z': 1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        # Its waiting for the avg acceleration to be low for 0.2 seconds
        time.sleep(0.2)
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        data['alt'] = data['alt'] - 10
        state = state.monitorPhase(data)
        # And for altitude to decrease
        self.assertEqual(str(state), 'DescentPhase')

        state = rocketState.SecondaryEnginePhase()
        data = {'acc_x': 1, 'acc_y': 1, 'acc_z': 1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        data['alt'] = data['alt'] -1005
        # will not set maxalt if accel is high
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.1, 'alt': 27125}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        time.sleep(0.2)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        # flag is now set
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase') #maxalt is now set
        # will detect missed apogee if 1000 feet below max alt
        data['alt'] = data['alt'] -1005
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')

        state = rocketState.SecondaryEnginePhase()
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.1, 'alt': 27123}
        state = state.monitorPhase(data)
        time.sleep(0.2)
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        data = {'acc_x': 1, 'acc_y': 1, 'acc_z': 1, 'alt': 27123}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')
        time.sleep(2.05)
        data['alt'] = data['alt'] -5
        # staying in high accel can remove low accel flag
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'SecondaryEnginePhase')

    def test_DescentPhase(self):
        state = rocketState.DescentPhase()
        data = {'acc_x': 0.1, 'acc_y': 0.1, 'acc_z': 0.7}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')
        data = {'acc_x': 0, 'acc_y': 0, 'acc_z': 1}
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'DescentPhase')
        time.sleep(5)
        state = state.monitorPhase(data)
        self.assertEqual(str(state), 'FinalPhase')


class TestMPU9250(unittest.TestCase):
    def test_read(self):
        piggy = pigpio.pi()
        mpuA = MPU9250.MPU9250(pi=piggy, gpio=17)
        for x in range(10):
            m1 = {}
            m1 = mpuA.read_all()
            # print(m1['acc_x'])
            self.assertTrue(m1['gyro_x'] < 10)
            self.assertTrue(m1['gyro_x'] > -10)
            self.assertTrue(m1['gyro_y'] < 10)
            self.assertTrue(m1['gyro_y'] > -10)
            self.assertTrue(m1['gyro_z'] < 10)
            self.assertTrue(m1['gyro_z'] > -10)
            self.assertTrue(m1['acc_x'] > -0.5)
            self.assertTrue(m1['acc_x'] < 0.5)
            self.assertTrue(m1['acc_y'] > -0.5)
            self.assertTrue(m1['acc_y'] < 0.5)
            self.assertTrue(m1['acc_z'] < 1.5)
            self.assertTrue(m1['acc_z'] > 0.5)

if __name__ == "__main__":
    unittest.main()

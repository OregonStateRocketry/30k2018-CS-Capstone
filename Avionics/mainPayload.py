import time, pigpio, os
import MPU9250, MPL3115A2, ESCMotor, PCF8523, payloadState

def mean_from_list(list):
    valid_terms = [x for x in list if x != 0]
    # Avoid divide by zero
    if valid_terms:
        return float(sum(valid_terms)) / len(valid_terms)
    return 0.0    # No valid numbers in this set


def setLinuxClock(newTime):
    ''' Set the current time from the PCF8523 '''
    print(newTime)
    # requires sudo
    # os.system('hwclock --set %s' % date_str)


class Payload(object):

    def __init__(self):
        # Most sensors share a pigpio object to control enable pins
        self.piggy = pigpio.pi()

        # Adjust orientation of certain payload sensors
        orient_A = {
            'gyro_x': ('gyro_x', -1),
            'gyro_y': ('gyro_z', -1),
            'gyro_z': ('gyro_y', -1),
            'acc_x' : ('acc_x',  -1),
            'acc_y' : ('acc_z',  -1),
            'acc_z' : ('acc_y',  -1)
        }
        orient_BC = {
            'gyro_x': ('gyro_x', 1),
            'gyro_y': ('gyro_z', 1),
            'gyro_z': ('gyro_y', -1),
            'acc_x' : ('acc_x',  1),
            'acc_y' : ('acc_z',  1),
            'acc_z' : ('acc_y',  -1)
        }

        # Use the GPIO number, NOT the pin number!
        self.mpuA = MPU9250.MPU9250(pi=self.piggy, gpio=17, orient=orient_A)
        self.mpuB = MPU9250.MPU9250(pi=self.piggy, gpio=27, orient=orient_BC)
        self.mpuC = MPU9250.MPU9250(pi=self.piggy, gpio=22, orient=orient_BC)

        # Get these IMU values from the Calibration/Calibrate.py script
        accel_17 = [ 4876, 6161, 8462]
        accel_27 = [-7058, 6056, 9173]
        accel_22 = [-3771, 7372, 9001]
        gyro_17  = [   40,  -13,    9]
        gyro_27  = [  -22,  -12,  -11]
        gyro_22  = [  -90,  -21,   46]


        # Apply calibration offsets into registers on the IMU
        self.mpuA.set_accel_calibration(accel_17[0],accel_17[1],accel_17[2])
        self.mpuA.set_gyro_calibration(gyro_17[0],gyro_17[1],gyro_17[2])
        self.mpuB.set_accel_calibration(accel_27[0],accel_27[1],accel_27[2])
        self.mpuB.set_gyro_calibration(gyro_27[0],gyro_27[1],gyro_27[2])
        self.mpuC.set_accel_calibration(accel_22[0],accel_22[1],accel_22[2])
        self.mpuC.set_gyro_calibration(gyro_22[0],gyro_22[1],gyro_22[2])


        self.mpl = MPL3115A2.MPL3115A2()
        self.mpl.setOffset(4639)
        self.clock = PCF8523.PCF8523()
        self.currentState = payloadState.PreLaunchPhase()
        #self.currentState = payloadState.ExperimentPhase()

        # Configure propeller ESC
        self.motor_propeller = ESCMotor.Motor(
            pi=self.piggy, pin=18,
            P=3.0, I=1.3, D=0.1, goal=0
            )     # semi-reasonable defaults?

        self.motor_counter = ESCMotor.Motor(
            pi=self.piggy, pin=13, DC=True, pinR=8,
            P=5.0, I=1.5, D=0.1, goal=0
            )     # semi-reasonable defaults?

        # Use GPIO 4 on breadboard for debugging
        self.DEBUG_GPIO = 4
        self.piggy.set_mode(self.DEBUG_GPIO, pigpio.OUTPUT)


    def logSensors(self, csv, sensors):
        ''' Write one line of sensor data to CSV '''
        sensors['time'] = time.time()
        csv.write("{state},{time:.4f},"
                  "{17_gyro_x:.3f},{17_gyro_y:.3f},{17_gyro_z:.3f},"
                  "{17_acc_x:.3f},{17_acc_y:.3f},{17_acc_z:.3f},"
                  "{27_gyro_x:.3f},{27_gyro_y:.3f},{27_gyro_z:.3f},"
                  "{27_acc_x:.3f},{27_acc_y:.3f},{27_acc_z:.3f},"
                  "{22_gyro_x:.3f},{22_gyro_y:.3f},{22_gyro_z:.3f},"
                  "{22_acc_x:.3f},{22_acc_y:.3f},{22_acc_z:.3f},"
                  "{acc_pid:.3f},{acc_pwm},"
                  "{gyro_pid:.3f},{gyro_pwm},"
                  "{temp:.2f},{alt}\n".format(**sensors)
                  )


    def runLoop(self, num=True):
        # Turn on LED on GPIO 4 to indicate program started
        self.piggy.write(self.DEBUG_GPIO, 1)

        with open("/home/pi/Avionics/av_payload.csv", "a+") as out:
            # Write a header line
            print("Running ESRA 30k payload avionics...\n")
            out.write(
                    "state,time,"
                    "17_gyro_x,17_gyro_y,17_gyro_z,"
                    "17_acc_x,17_acc_y,17_acc_z,"
                    "27_gyro_x,27_gyro_y,27_gyro_z,"
                    "27_acc_x,27_acc_y,27_acc_z,"
                    "22_gyro_x,22_gyro_y,22_gyro_z,"
                    "22_acc_x,22_acc_y,22_acc_z,"
                    "acc_pid,acc_pwm,"
                    "gyro_pid,gyro_pwm,"
                    "temp(c),alt(ft)\n"
                  )

            while(num):
                if num is not True: num -= 1
                # Build a new dictionary of sensor data for this sample
                data = {}
                for x,y in [('17_',self.mpuA), ('27_', self.mpuB), ('22_', self.mpuC)]:
                  data.update( {x+k:v for k,v in y.read_all().items()} )

                data['temp'], data['alt'] = self.mpl.readTempAlt()

                data['acc_x'] = mean_from_list(
                    ( data['17_acc_x'], data['27_acc_x'], data['22_acc_x'] )
                )
                data['acc_y'] = mean_from_list(
                    ( data['17_acc_y'], data['27_acc_y'], data['22_acc_y'] )
                )
                data['acc_z'] = mean_from_list(
                    ( data['17_acc_z'], data['27_acc_z'], data['22_acc_z'] )
                )
                data['gyro_x'] = mean_from_list(
                    ( data['17_gyro_x'], data['27_gyro_x'], data['22_gyro_x'] )
                )
                if(data['temp'] > 9000):
                    #if altimeter shuts down, stop running motor immediately
                    self.currentState = payloadState.DescentPhase()
                if str(self.currentState) == 'ExperimentPhase':
                    # Recalculate propeller motor speed using latest acceleration
                    data['acc_pid'], data['acc_pwm'] = self.motor_propeller.update_motor(
                        data['acc_z']
                    )
                    # Recalculate counterweight motor speed using latest gyro
                    data['gyro_pid'], data['gyro_pwm'] = self.motor_counter.update_motor(
                        data['gyro_x']
                    )
                else:
                    # Ensure the motors are stopped after the experiment
                    if str(self.currentState) == 'DescentPhase':
                        self.motor_propeller.stop()
                        self.motor_counter.stop()
                    data['acc_pid']  = 0
                    data['acc_pwm']  = 0
                    data['gyro_pid'] = 0
                    data['gyro_pwm'] = 0

                self.currentState = self.currentState.monitorPhase(data)
                data['state'] = self.currentState.stateNum

                self.logSensors(out, data)

        # Turn off LED on GPIO 4 to indicate program finished
        self.piggy.write(self.DEBUG_GPIO, 0)


if __name__ == "__main__":
    payload = Payload()
    payload.runLoop(True)

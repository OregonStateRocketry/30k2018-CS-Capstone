import time, pigpio, os
import MPU9250, MPL3115A2, ESCMotor, PCF8523, payloadState

def avg_three(z1, z2, z3):
    return ((z1+z2+z3) / 3.0)


def setLinuxClock(newTime):
    ''' Set the current time from the PCF8523 '''
    print(newTime)
    # requires sudo
    # os.system('hwclock --set %s' % date_str)


class Payload(object):

    def __init__(self):
        # Most sensors share a pigpio object to control enable pins
        self.piggy = pigpio.pi()

        # Use the GPIO number, NOT the pin number!
        self.mpuA = MPU9250.MPU9250(pi=self.piggy, gpio=17)
        #mpuB = MPU6050.MPU6050(pi=piggy, gpio=27)
        #mpuC = MPU6050.MPU6050(pi=piggy, gpio=22)

        self.mpl = MPL3115A2.MPL3115A2()
        self.clock = PCF8523.PCF8523()
        self.currentState = payloadState.PreLaunchPhase()

        # Configure propeller ESC
        self.motor_propeller = ESCMotor.Motor(
            pi=self.piggy, pin=18,
            P=1.2, I=0.5, D=0.1, Z=1
            )     # semi-reasonable defaults?

        self.motor_counter = ESCMotor.Motor(
            pi=self.piggy, pin=13,
            P=1.2, I=1, D=0.5, Z=0
            )     # semi-reasonable defaults?

        # Use GPIO 4 on breadboard for debugging
        self.DEBUG_GPIO = 4
        self.piggy.set_mode(self.DEBUG_GPIO, pigpio.OUTPUT)

    def logSensors(self, csv, sensors):
        ''' Write one line of sensor data to CSV '''
        sensors['time'] = time.time()
        if len(sensors) > 10:
            csv.write("{state},{time:.4f},"
                      "{gyro_x:.3f},{gyro_y:.3f},{gyro_z:.3f},"
                      "{acc_x:.3f},{acc_y:.3f},{acc_z:.3f},"
                      "{temp:.2f},{alt},"
                      "{acc_pid:.3f},{acc_pwm},"
                      "{gyro_pid:.3f},{gyro_pwm}\n".format(**sensors)
                      )
        else:
            csv.write("{state},{time:.4f},"
                      "{gyro_x:.3f},{gyro_y:.3f},{gyro_z:.3f},"
                      "{acc_x:.3f},{acc_y:.3f},{acc_z:.3f},"
                      "{temp:.2f},{alt}\n".format(**sensors)
                      )

    def runLoop(self, num=True):
        # Turn on LED on GPIO 4 to indicate program started
        self.piggy.write(self.DEBUG_GPIO, 1)

        with open("av_out.csv", "a+") as out:
            # Write a header line
            print("Running ESRA 30k payload avionics...\n")
            out.write(
                    "gyro_x,gyro_y,gyro_z,"
                    "acc_x,acc_y,acc_z,"
                    "temp(c),alt(m),"
                    "acc_pid,acc_pwm,"
                    "gyro_pid,gyro_pwm\n"
                  )

            while(num):
                if num is not True: num -= 1
                # Build a new dictionary of sensor data for this sample
                data = self.mpuA.read_all()
                data['temp'], data['alt'] = self.mpl.readTempAlt()

                self.currentState = self.currentState.monitorPhase(data)
                data['state'] = self.currentState.stateNum

                if self.currentState == 'ExperimentPhase':
                    # Recalculate propeller motor speed using latest acceleration
                    # avg_acc_z = avg_three(m1['acc_z'], m2['acc_z'], m3['acc_z'])
                    data['acc_pid'], data['acc_pwm'] = self.motor_propeller.update_motor(
                            data['acc_z']
                        )

                    # Recalculate counterweight motor speed using latest gyro
                    # avg_gyro = avg_three(m1['gyro_z'], m2['gyro_z'], m3['gyro_z'])
                    data['gyro_pid'], data['gyro_pwm'] = self.motor_counter.update_motor(
                            data['gyro_x']
                        )

                self.logSensors(out, data)

        # Turn off LED on pin 7 to indicate program finished
        self.piggy.write(self.DEBUG_GPIO, 0)


if __name__ == "__main__":
    payload = Payload()
    payload.runLoop(5)

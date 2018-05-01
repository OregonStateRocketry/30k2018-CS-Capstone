import time, pigpio, os
import MPU9250, MPL3115A2, PCF8523, rocketState


def avg_three(z1, z2, z3):
    return ((z1+z2+z3) / 3.0)


def setLinuxClock(newTime):
    ''' Set the current time from the PCF8523 '''
    print(newTime)
    # requires sudo
    # os.system('hwclock --set %s' % date_str)


class Rocket(object):
    def __init__(self):
        # Most sensors share a pigpio object to control enable pins
        self.piggy = pigpio.pi()
        Orientation = {
                'gyro_x': ('gyro_z', -1),
                'gyro_y': ('gyro_y', 1),
                'gyro_z': ('gyro_x', 1),
                'acc_x' : ('acc_z',  -1),
                'acc_y' : ('acc_y',  1),
                'acc_z' : ('acc_x',  1)
            }
        accel_17=[-5495,4982,9098]
        accel_27=[-5708,-5757,9744]
        accel_22=[-4053,-4382,8801]
        gyro_17=[23,-16,12]
        gyro_27=[3,-18,-2]
        gyro_22=[-3,-24,7]
        # Use the GPIO number, NOT the pin number!
        self.mpuA = MPU9250.MPU9250(pi=self.piggy, gpio=17,orient=Orientation)
        self.mpuB = MPU9250.MPU9250(pi=self.piggy, gpio=27,orient=Orientation)
        self.mpuC = MPU9250.MPU9250(pi=self.piggy, gpio=22,orient=Orientation)
        self.mpuA.set_accel_calibration(accel_17[0],accel_17[1],accel_17[2])
        self.mpuA.set_gyro_calibration(gyro_17[0],gyro_17[1],gyro_17[2])
        self.mpuB.set_accel_calibration(accel_27[0],accel_27[1],accel_27[2])
        self.mpuB.set_gyro_calibration(gyro_27[0],gyro_27[1],gyro_27[2])
        self.mpuC.set_accel_calibration(accel_22[0],accel_22[1],accel_22[2])
        self.mpuC.set_gyro_calibration(gyro_22[0],gyro_22[1],gyro_22[2])
        self.mpl = MPL3115A2.MPL3115A2()
        self.mpl.setOffset(235)
        self.clock = PCF8523.PCF8523()
        self.currentState = rocketState.PreLaunchPhase()

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
                  "{temp:.2f},{alt}\n".format(**sensors)
                  )

    def runLoop(self, num=True):
        # Turn on LED on GPIO 4 to indicate program started
        self.piggy.write(self.DEBUG_GPIO, 1)

        with open("av_rocket.csv", "a+") as out:
            # Write a header line
            print("Running ESRA 30k rocket avionics...\n")
            out.write(
                    "state,time,"
                    "17_gyro_x,17_gyro_y,17_gyro_z,"
                    "17_acc_x,17_acc_y,17_acc_z,"
                    "27_gyro_x,27_gyro_y,27_gyro_z,"
                    "27_acc_x,27_acc_y,27_acc_z,"
                    "22_gyro_x,22_gyro_y,22_gyro_z,"
                    "22_acc_x,22_acc_y,22_acc_z,"
                    "temp(c),alt(ft)\n"
                  )

            while(num):
                if num is not True: num -= 1
                # Build a new dictionary of sensor data for this sample
                data = {}
                # Try something like:
                # {'b_'+k:v for k,v in a.items()}
                for x,y in [('17_',self.mpuA), ('27_', self.mpuB), ('22_', self.mpuC)]:
                  data.update( {x+k:v for k,v in y.read_all().items()} )

                data['acc_x'] = avg_three(
                    data['17_acc_x'], data['27_acc_x'], data['22_acc_x']
                    )
                data['acc_y'] = avg_three(
                    data['17_acc_y'], data['27_acc_y'], data['22_acc_y']
                    )
                data['acc_z'] = avg_three(
                    data['17_acc_z'], data['27_acc_z'], data['22_acc_z']
                    )

                data['temp'], data['alt'] = self.mpl.readTempAlt()

                self.currentState = self.currentState.monitorPhase(data)
                data['state'] = self.currentState.stateNum

                self.logSensors(out, data)
                # print(data)

        # Turn off LED on pin 7 to indicate program finished
        self.piggy.write(self.DEBUG_GPIO, 0)


if __name__ == "__main__":
    rocket = Rocket()
    rocket.runLoop(100)

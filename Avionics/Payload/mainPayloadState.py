import time, pigpio, os
import MPU9250, MPL3115A2, ESCMotor, PCF8523, payloadState

# Most sensors share a pigpio object to control enable pins
piggy = pigpio.pi()

# Use the GPIO number, NOT the pin number!
mpuA = MPU9250.MPU9250(pi=piggy, gpio=17)
#mpuB = MPU6050.MPU6050(pi=piggy, gpio=27)
#mpuC = MPU6050.MPU6050(pi=piggy, gpio=22)

mpl = MPL3115A2.MPL3115A2()

# currentState = payloadState.PayloadState()

clock = PCF8523.PCF8523()

# Configure propeller ESC
motor_propeller = ESCMotor.Motor(
    pi=piggy, pin=18,
    P=1.2, I=0.5, D=0.1, Z=1
    )     # semi-reasonable defaults?

motor_counter = ESCMotor.Motor(
    pi=piggy, pin=13,
    P=1.2, I=1, D=0.5, Z=0
    )     # semi-reasonable defaults?

# Use GPIO 4 on breadboard for debugging
DEBUG_GPIO = 4
piggy.set_mode(DEBUG_GPIO, pigpio.OUTPUT)


def avg_three(z1, z2, z3):
    return ((z1+z2+z3) / 3.0)


def setLinuxClock():
    ''' Set the current time from the PCF8523 '''
    print(clock.gettime())
    # requires sudo
    # os.system('hwclock --set %s' % date_str)

def logSensors(csv, sensors):
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

def runLoop():
    # Turn on LED on GPIO 4 to indicate program started
    piggy.write(DEBUG_GPIO, 1)
    currentState = payloadState.PreLaunchPhase()

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

        for x in range(1000):
            # Build a new dictionary of sensor data for this sample
            data = mpuA.read_all()

            data['temp'], data['alt'] = mpl.readTempAlt()

            currentState = currentState.monitorPhase(data)
            data['state'] = currentState.stateNum

            if currentState == 'ExperimentPhase':
                # Recalculate propeller motor speed using latest acceleration
                # avg_acc_z = avg_three(m1['acc_z'], m2['acc_z'], m3['acc_z'])
                data['acc_pid'], data['acc_pwm'] = motor_propeller.update_motor(
                        data['acc_z']
                    )

                # Recalculate counterweight motor speed using latest gyro
                # avg_gyro = avg_three(m1['gyro_z'], m2['gyro_z'], m3['gyro_z'])
                data['gyro_pid'], data['gyro_pwm'] = motor_counter.update_motor(
                        data['gyro_x']
                    )

            logSensors(out, data)

    # Turn off LED on pin 7 to indicate program finished
    piggy.write(DEBUG_GPIO, 0)


if __name__ == "__main__":
    runLoop()

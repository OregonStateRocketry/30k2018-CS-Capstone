import time, pigpio
import MPU6050, ESCMotor

# Most sensors share a pigpio object to control enable pins
piggy = pigpio.pi()

# Use the GPIO number, NOT the pin number!
mpuA = MPU6050.MPU6050(pi=piggy, gpio=17)
mpuB = MPU6050.MPU6050(pi=piggy, gpio=27)
mpuC = MPU6050.MPU6050(pi=piggy, gpio=22)

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


def runLoop():
    # Turn on LED on GPIO 4 to indicate program started
    piggy.write(DEBUG_GPIO, 1)

    with open("av_out.csv", "w") as out:
        # Write a header line
        # print("Payload_Avionics\n")
        out.write("{},{},{},{},{},"
              "{},{},{},{},{},"
              "{},{},{},{},{},"
              "{},{}\n".format(
                  'm1.roll(rad)', 'm1.pitch(rad)', 'm1.ax', 'm1.ay', 'm1.az',
                  'm2.roll(rad)', 'm2.pitch(rad)', 'm2.ax', 'm2.ay', 'm2.az',
                  'm3.roll(rad)', 'm3.pitch(rad)', 'm3.ax', 'm3.ay', 'm3.az',
                  'temp(c)', 'p(mbar)'
                  )
              )

        for x in range(1000):
            # Refresh the MPU readings
            m1 = mpuA.read_all()
            m2 = mpuB.read_all()
            m3 = mpuC.read_all()

            # Recalculate propeller motor speed using latest acceleration
            avg_acc_z = avg_three(m1['acc_z'], m2['acc_z'], m3['acc_z'])
            acc_pid, acc_pwm = motor_propeller.update_motor(avg_acc_z)

            # Recalculate counterweight motor speed using latest gyro
            avg_gyro = avg_three(m1['gyro_z'], m2['gyro_z'], m3['gyro_z'])
            gyro_pid, gyro_pwm = motor_counter.update_motor(avg_gyro)

            # Get latest temp and pressure
            # temp, pressure = bmp180.readBmp180()

            out.write("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"
                  "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"
                  "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"
                  # "{:.3f},{:.3f},"
                  "\t{:.3f},{:.2f},{}"
                  "\t{:.3f},{:.2f},{}\n".format(
                      m1['gyro_x'], m1['gyro_y'], m1['gyro_z'],
                      m1['acc_x'],  m1['acc_y'],  m1['acc_z'],
                      m2['gyro_x'], m2['gyro_y'], m2['gyro_z'],
                      m2['acc_x'],  m2['acc_y'],  m2['acc_z'],
                      m3['gyro_x'], m3['gyro_y'], m3['gyro_z'],
                      m3['acc_x'],  m3['acc_y'],  m3['acc_z'],
                      # temp, pressure,
                      avg_acc_z, acc_pid, acc_pwm,
                      avg_gyro, gyro_pid, gyro_pwm
                      )
                  )

    # Turn off LED on pin 7 to indicate program finished
    piggy.write(DEBUG_GPIO, 0)

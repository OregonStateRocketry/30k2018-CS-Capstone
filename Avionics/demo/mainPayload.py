import time, pigpio
import MPU6050, BMP180, ESCMotor

# Most sensors share a pigpio object to control enable pins
piggy = pigpio.pi()

# Use the GPIO number, NOT the pin number!
mpuA = MPU6050.MPU6050(pi=piggy, pin=17)
mpuB = MPU6050.MPU6050(pi=piggy, pin=27)
mpuC = MPU6050.MPU6050(pi=piggy, pin=22)

bmp180 = BMP180.BMP180(address=0x77)

# Configure propeller ESC
motor_propeller = ESCMotor.Motor(
    pi=piggy, pin=18,
    P=1.2, I=0.5, D=0.1, Z=1
    )     # semi-reasonable defaults?

motor_counter = ESCMotor.Motor(
    pi=piggy, pin=13,
    P=1.2, I=1, D=0.5, Z=0
    )     # semi-reasonable defaults?

# Use pin 7 on breadboard for debugging
DEBUG_PIN = 7
piggy.set_mode(DEBUG_PIN, pigpio.OUTPUT)
# GPIO.setup(7, GPIO.OUT)         # breadboard LED used for debugging


def avg_three(z1, z2, z3):
    return ((z1+z2+z3) / 3.0)


def runLoop():
    # Turn on LED on pin 7 to indicate program started
    piggy.write(DEBUG_PIN, 1)
    # GPIO.output(7, 1)

    # Write a header line
    print("Payload_Avionics\n")
    print("{},{},{},{},{},"
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
        temp, pressure = bmp180.readBmp180()

        # Debugging
        # print("{:8.3f},{:8.2f},{:8}\t|\t{:8.3f},{:8.2f},{:8}".format(
        #       avg_acc_z, acc_pid, acc_pwm,
        #       avg_gyro, gyro_pid, gyro_pwm,
        #       )
        # )

        print("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"
              "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"
              "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"
              "{:.3f},{:.3f},"
              "\t{:.3f},{:.2f},{}"
              "\t{:.3f},{:.2f},{}".format(
                  m1['gyro_x'], m1['gyro_y'], m1['gyro_z'],
                  m1['acc_x'],  m1['acc_y'],  m1['acc_z'],
                  m2['gyro_x'], m2['gyro_y'], m2['gyro_z'],
                  m2['acc_x'],  m2['acc_y'],  m2['acc_z'],
                  m3['gyro_x'], m3['gyro_y'], m3['gyro_z'],
                  m3['acc_x'],  m3['acc_y'],  m3['acc_z'],
                  temp, pressure,
                  avg_acc_z, acc_pid, acc_pwm,
                  avg_gyro, gyro_pid, gyro_pwm
                  )
              )


if __name__ == "__main__":
    runLoop()
    # try:
    # except Exception as e:
    #     piggy.write(DEBUG_PIN, 0)
    #     print(e)
    #     # GPIO.output(7, 0)
    #     print("Done!")

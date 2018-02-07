import time, pigpio
# import RPi.GPIO as GPIO
import MPU6050, BMP180, ESCMotor, PID

# Both motors share a pigpio object
piggy = pigpio.pi()

# Use the PIN number, NOT the GPIO number!
mpuA = MPU6050.MPU6050(address=0x69, enable_pin=11)
mpuB = MPU6050.MPU6050(address=0x69, enable_pin=13)
mpuC = MPU6050.MPU6050(address=0x69, enable_pin=11)

bmp180 = BMP180.BMP180(address=0x77)

# Configure propeller ESC
motor_propeller = ESCMotor.Motor(
    pi=piggy, pin=18,
    P=4.0, I=0.4, D=1.2, Z=0.0)     # semi-reasonable defaults

# Use pin 7 on breadboard for debugging
DEBUG_PIN = 7
piggy.set_mode(DEBUG_PIN, pigpio.OUTPUT)
# GPIO.setup(7, GPIO.OUT)         # breadboard LED used for debugging

def avg_acc(z1, z2, z3):
    return (z1+z2+z3) / 3.0

def runLoop():
    # Turn on LED on pin 7 to indicate program started
    piggy.write(DEBUG_PIN, 1)
    # GPIO.output(7, 1)

    # Write a header line
    print("Payload_Avionics\n")
    print("{},{},{},{},{},"\
          "{},{},{},{},{},"\
          "{},{},{},{},{},"\
          "{},{}\n".format(
          'm1.roll(rad)', 'm1.pitch(rad)', 'm1.ax', 'm1.ay', 'm1.az',
          'm2.roll(rad)', 'm2.pitch(rad)', 'm2.ax', 'm2.ay', 'm2.az',
          'm3.roll(rad)', 'm3.pitch(rad)', 'm3.ax', 'm3.ay', 'm3.az',
          'temp(c)', 'p(mbar)'
    ))

    while True:
        # Refresh the MPU readings
        m1 = mpuA.read_most()
        m2 = mpuB.read_most()
        m3 = mpuC.read_most()

        # Run the PID loop
        avg_acc_z = avg_acc(m1['acc_z'] + m2['acc_z'] + m3['acc_z'])
        # Recalculate motor speed using latest acceleration
        motor_propeller.update_motor(avg_acc_z)

        temp, pressure = bmp180.readBmp180()

        print("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"\
              "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"\
              "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},"\
              "{:.3f},{:.3f}".format(
            m1['roll'], m1['pitch'], m1['acc_x'], m1['acc_y'], m1['acc_z'],
            m2['roll'], m2['pitch'], m2['acc_x'], m2['acc_y'], m2['acc_z'],
            m3['roll'], m3['pitch'], m3['acc_x'], m3['acc_y'], m3['acc_z'],
            temp, pressure
        ))

if __name__ == "__main__":
    try:
        runLoop()
    except:
        piggy.write(DEBUG_PIN, 0)
        # GPIO.output(7, 0)
        print("Done!")

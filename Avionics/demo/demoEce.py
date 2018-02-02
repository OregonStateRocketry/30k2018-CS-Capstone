from MPU6050 import MPU6050
import RPi.GPIO as GPIO
from BMP180 import BMP180
import time

# Use the PIN number, NOT the GPIO number!
mpuA = MPU6050(0x69, 11)
mpuB = MPU6050(0x69, 13)
mpuC = MPU6050(0x69, 15)
bmp180 = BMP180(address=0x77)

GPIO.setup(7, GPIO.OUT)

def runSensors():
    # Turn on LED on pin 4 to show that it's recording:
    GPIO.output(7, 1)

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
        runSensors()
    except:
        GPIO.output(7, 0)
        print("Done!")

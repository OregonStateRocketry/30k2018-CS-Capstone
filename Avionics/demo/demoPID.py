from MPU6050 import MPU6050
from PID import PID
import RPi.GPIO as GPIO
import time

# These are using GPIO.BOARD, use the PIN number, NOT the GPIO number!
mpuA = MPU6050(0x69, 11)
mpuB = MPU6050(0x69, 13)
mpuC = MPU6050(0x69, 15)

pid = PID(P=4, I=0.4, D=1.2)
pid.setPoint(0.0)

# debugging LED
GPIO.setup(7, GPIO.OUT)

def get_avg_z():
    total_z = 0
    for x in [mpuA, mpuB, mpuC]:
        x.read_raw_data()
        total_z += x.read_scaled_accel_z()
    return total_z / 3.0

def pid_to_pwm(p):
    pwm_min, pwm_max = 1000, 2000
    pid_min, pid_max = 0.0, 3.0
    if p<pid_min: p = pid_min
    if p>pid_max: p = pid_max
    pid_range = (pid_max - pid_min)
    pwm_range = (pwm_max - pwm_min)
    return (((p - pid_min) * pwm_range) / pid_range) + pwm_min

while True:
    avg_z = get_avg_z()
    pid_out = -pid.update(avg_z)
    pwm_out = pid_out
    print("acc_z = {:.3f},\tpid = {:.3f},\tpwm = {}".format(
        avg_z, pid_out, pid_to_pwm(pid_out))
    )
    time.sleep(1)

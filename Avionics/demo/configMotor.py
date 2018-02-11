import sys, time, pigpio, ESCMotor

piggy = pigpio.pi()

m1 = ESCMotor.Motor(pi=piggy, pin=18)
# motor_counter = ESCMotor.Motor(pi=piggy, pin=13)

# print("Calibrating ESC..")
# m1.set_ESC_range()

print("Running motor demo:\n")
while True:
    for n in range(50):
        m1.set_motor(1000+n*20)
        print("."*n)
        sys.stdout.write("\033[F") # Cursor up one line
        # sys.stdout.write("\033[K") # Clear to the end of line
        # pi.set_servo_pulsewidth(PIN, 1010+20*n)
        time.sleep(0.05)

    for n in range(50, 0, -1):
        m1.set_motor(1000+n*20)
        print("."*n)
        sys.stdout.write("\033[F") # Cursor up one line
        sys.stdout.write("\033[K") # Clear to the end of line
        # pi.set_servo_pulsewidth(PIN, 1010+20*n)
        time.sleep(0.05)

# import pigpio, time
import time, sys

class Motor(object):
    '''Tools to control and interface with the ESC and brushless motor'''
    def __init__(self, pi, pin):
        self.PIN = 18
        self.curSpeed = 1000

        if not pi:
            self.pi = pigpio.pi()

        self.pi.set_mode(PIN, pigpio.OUTPUT)

    def configure(self, min=1000, max=2000):
        '''Configure input range on ESC, needs to run while ESC is starting'''
        print("Configuring ESC range - Plug in ESC now!")
        pi.set_servo_pulsewidth(PIN, 2000)
        time.sleep(10)
        pi.set_servo_pulsewidth(PIN, 1000)
        print("ESC range has been set.")

if __name__ == "__main__":

    print("Running ESC/motor demo..")
    curSpeed = 1000
    dSpeed = 50

    print("Running motor demo")
    while True:
        for n in range(50):
            print("."*n)
            sys.stdout.write("\033[F") # Cursor up one line
            # sys.stdout.write("\033[K") # Clear to the end of line
            # pi.set_servo_pulsewidth(PIN, 1010+20*n)
            time.sleep(0.05)

        for n in range(50, 0, -1):
            print("."*n)
            sys.stdout.write("\033[F") # Cursor up one line
            sys.stdout.write("\033[K") # Clear to the end of line
            # pi.set_servo_pulsewidth(PIN, 1010+20*n)
            time.sleep(0.05)

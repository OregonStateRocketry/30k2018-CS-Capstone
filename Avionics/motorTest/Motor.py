import pigpio, time

PIN = 18

pi = pigpio.pi()
pi.set_mode(PIN, pigpio.OUTPUT)

# print("Initializing ESC.")
# print(2000)
# pi.set_servo_pulsewidth(PIN, 2000)
# time.sleep(10)
# print(1000)
# pi.set_servo_pulsewidth(PIN, 1000)
# time.sleep(3)
# print(1200)
# pi.set_servo_pulsewidth(PIN, 1200)
# time.sleep(3)
# print(0)
# pi.set_servo_pulsewidth(PIN, 0)
# print("Running loop.")

pi.set_servo_pulsewidth(PIN, 1000)
time.sleep(10)

speed = 1000
dSpeed = 50

while True:
    print(speed)
    pi.set_servo_pulsewidth(PIN, speed)
    time.sleep(0.2)
    speed += dSpeed
    if speed > 2000 or speed < 1000:
        dSpeed *= -1
        speed  += 2*dSpeed

pi.stop()

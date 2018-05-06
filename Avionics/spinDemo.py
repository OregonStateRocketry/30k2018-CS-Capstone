import pigpio, time
import MPU9250, ESCMotor

def avg_three(z1, z2, z3):
    return ((z1+z2+z3) / 3.0)

piggy = pigpio.pi()

# Adjust orientation of certain payload sensors
orient_A = {
    'gyro_x': ('gyro_x', -1),
    'gyro_y': ('gyro_z', -1),
    'gyro_z': ('gyro_y', 1),
    'acc_x' : ('acc_x',  -1),
    'acc_y' : ('acc_z',  -1),
    'acc_z' : ('acc_y',  1)
}
orient_BC = {
    'gyro_x': ('gyro_x', -1),
    'gyro_y': ('gyro_z', 1),
    'gyro_z': ('gyro_y', -1),
    'acc_x' : ('acc_x',  -1),
    'acc_y' : ('acc_z',  1),
    'acc_z' : ('acc_y',  -1)
}

mpuA = MPU9250.MPU9250(pi=piggy, gpio=17, orient=orient_A)
mpuB = MPU9250.MPU9250(pi=piggy, gpio=27, orient=orient_BC)
mpuC = MPU9250.MPU9250(pi=piggy, gpio=22, orient=orient_BC)

# Get these IMU values from the Calibration/Calibrate.py script
accel_17 = [ 4883, 6144, 8468]
accel_27 = [-7065, 6068, 9173]
accel_22 = [-3779, 7385, 9001]
gyro_17  = [   34,  -11,   24]
gyro_27  = [  -28,   -2,  -16]
gyro_22  = [  -90,  -16,   38]

# Apply calibration offsets into registers on the IMU
mpuA.set_accel_calibration(accel_17[0],accel_17[1],accel_17[2])
mpuA.set_gyro_calibration(gyro_17[0],gyro_17[1],gyro_17[2])
mpuB.set_accel_calibration(accel_27[0],accel_27[1],accel_27[2])
mpuB.set_gyro_calibration(gyro_27[0],gyro_27[1],gyro_27[2])
mpuC.set_accel_calibration(accel_22[0],accel_22[1],accel_22[2])
mpuC.set_gyro_calibration(gyro_22[0],gyro_22[1],gyro_22[2])

# Configure propeller ESC
motor_propeller = ESCMotor.Motor(
    pi=piggy, pin=18,
    P=3.0, I=1.3, D=0.1, goal=0
    )     # semi-reasonable defaults?

motor_counter = ESCMotor.Motor(
    pi=piggy, pin=13, DC=True, pinR=8,
    P=5.0, I=1.5, D=0.1, goal=0
    )     # semi-reasonable defaults?

while True:
    # Build a new dictionary of sensor data for this sample
    data = {}
    for x,y in [('17_',mpuA), ('27_', mpuB), ('22_', mpuC)]:
      data.update( {x+k:v for k,v in y.read_all().items()} )

    data['acc_z'] = avg_three(
        data['17_acc_z'], data['27_acc_z'], data['22_acc_z']
    )
    data['gyro_x'] = avg_three(
        data['17_gyro_x'], data['27_gyro_x'], data['22_gyro_x']
    )

    # Recalculate propeller motor speed using latest acceleration
    data['acc_pid'], data['acc_pwm'] = motor_propeller.update_motor(
        data['acc_z']
    )
    # Recalculate counterweight motor speed using latest gyro
    data['gyro_pid'], data['gyro_pwm'] = motor_counter.update_motor(
        data['gyro_x']
    )

    # print(data['17_acc_z'], data['27_acc_z'], data['22_acc_z'])

    print("Propeller [{:.4f} -> ({:.4f}, {})], " \
        "Counterweight [{:.4f} -> ({:.4f}, {})]\n".format(
            data['acc_z'], data['acc_pid'], data['acc_pwm'],
            data['gyro_x'], data['gyro_pid'], data['gyro_pwm']
    ))

    time.sleep(0.1)

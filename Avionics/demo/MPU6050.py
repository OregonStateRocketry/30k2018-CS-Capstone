import pigpio
import smbus


class MPU6050(object):
    PWR_MGMT_1 = 0x6b

    GYRO_CONFIG = 0x1B
    FS_250 = 0
    FS_500 = 1
    FS_1000 = 2
    FS_2000 = 3

    ACCEL_CONFIG = 0x1C
    AFS_2g = 0
    AFS_4g = 1
    AFS_8g = 2
    AFS_16g = 3

    ACCEL_SCALE = {
        AFS_2g  : [ 2, 16384.0],
        AFS_4g  : [ 4, 8192.0],
        AFS_8g  : [ 8, 4096.0],
        AFS_16g : [16, 2048.0]
        }

    TEMP_START_BLOCK = 0x41
    GYRO_START_BLOCK = 0x43
    ACCEL_START_BLOCK = 0x3B

    GYRO_SCALE = {
        FS_250  : [ 250, 131.0],
        FS_500  : [ 500, 65.5],
        FS_1000 : [1000, 32.8],
        FS_2000 : [2000, 16.4]
        }

    DICT_HEADER = 'gyro_x gyro_y gyro_z acc_x acc_y acc_z'.split()

    def __init__(self, pi, pin, address=0x69,
                 fs_scale=FS_250, afs_scale=AFS_2g,
                 bus=1
                 ):
        self.pi = pi
        self.bus = smbus.SMBus(1)

        self.address = address
        self.pin = pin
        self.fs_scale = fs_scale
        self.afs_scale = afs_scale

        # Enable output pin via pigpio
        self.pi.set_mode(self.pin, pigpio.OUTPUT)

        # Set this sensor's address to 0x69 to distinguish it
        self.enable_sensor()
        # We need to wake up the module as it start in sleep mode
        self.bus.write_byte_data(self.address, MPU6050.PWR_MGMT_1, 0x00)
        # Set the gryo resolution
        self.bus.write_byte_data(
            self.address, MPU6050.GYRO_CONFIG, self.fs_scale << 3
            )
        # Set the accelerometer resolution
        self.bus.write_byte_data(
            self.address, MPU6050.ACCEL_CONFIG, self.afs_scale << 3
            )
        # Set this sensor's address back to 0x68 with the others
        self.disable_sensor()

    def enable_sensor(self):
        ''' Pull this sensor's enable pin HIGH '''
        self.pi.write(self.pin, 1)

    def disable_sensor(self):
        ''' Pull this sensor's enable pin LOW '''
        self.pi.write(self.pin, 0)

    def read_acc_gyro(self):
        ''' Read block containing both gyro and accelerometer values '''
        self.enable_sensor()

        # Raw reads 14 bytes = 6 bytes accel + 2 bytes temp + 6 bytes gyro
        raw = self.bus.read_i2c_block_data(
            self.address, self.ACCEL_START_BLOCK, 14
            )

        self.disable_sensor()

        # Accel contains 6 bytes total beginning at 0x3b
        self.accel_scaled_x = self.scale_accel(
            self.twos_compliment(raw[0], raw[1])
            )
        self.accel_scaled_y = self.scale_accel(
            self.twos_compliment(raw[2], raw[3])
            )
        self.accel_scaled_z = self.scale_accel(
            self.twos_compliment(raw[4], raw[5])
            )

        # If you want temperature, grab bytes 6 and 7

        # Gyro contains 6 bytes total beginning at 0x43
        self.gyro_scaled_x = self.scale_gyro(
            self.twos_compliment(raw[8],  raw[9])
            )
        self.gyro_scaled_y = self.scale_gyro(
            self.twos_compliment(raw[10], raw[11])
            )
        self.gyro_scaled_z = self.scale_gyro(
            self.twos_compliment(raw[12], raw[13])
            )

    def scale_accel(self, raw_acc):
        ''' Convert raw acceleration value to m/s^2 '''
        return raw_acc / MPU6050.ACCEL_SCALE[self.afs_scale][1]

    def scale_gyro(self, raw_gyro):
        ''' Convert raw gyro value to rad/s '''
        return raw_gyro / MPU6050.GYRO_SCALE[self.fs_scale][1]

    def twos_compliment(self, high_byte, low_byte):
        ''' Combine two bytes using twos complement '''
        value = (high_byte << 8) + low_byte
        if (value >= 0x8000):
            return -((0xffff - value) + 1)
        return value

    def refresh_data(self):
        ''' Read the raw data from the sensor and convert units '''
        self.enable_sensor()
        self.read_acc_gyro()    # Also does unit conversions
        self.disable_sensor()

    def read_all(self):
        ''' Return dictionary of acceleration (m/s^2) and gyro (rad/s) '''
        self.refresh_data()
        return dict(zip(MPU6050.DICT_HEADER, (
            self.gyro_scaled_x,
            self.gyro_scaled_y,
            self.gyro_scaled_z,
            self.accel_scaled_x,
            self.accel_scaled_y,
            self.accel_scaled_z
        )))


if __name__ == "__main__":
    piggy = pigpio.pi()

    mpuA = MPU6050(pi=piggy, pin=17)
    mpuB = MPU6050(pi=piggy, pin=27)
    mpuC = MPU6050(pi=piggy, pin=22)

    for x in range(1000):
        m1 = mpuA.read_all()
        m2 = mpuB.read_all()
        m3 = mpuC.read_all()

        print("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\t"
              "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\t"
              "{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}".format(
                  m1['gyro_x'], m1['gyro_y'], m1['gyro_z'],
                  m1['acc_x'], m1['acc_y'], m1['acc_z'],
                  m2['gyro_x'], m2['gyro_y'], m2['gyro_z'],
                  m2['acc_x'], m2['acc_y'], m2['acc_z'],
                  m3['gyro_x'], m3['gyro_y'], m3['gyro_z'],
                  m3['acc_x'], m3['acc_y'], m3['acc_z'])
              )

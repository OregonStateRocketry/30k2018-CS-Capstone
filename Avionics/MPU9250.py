import pigpio
import smbus


class MPU9250(object):
    PWR_MGMT_1 = 0x6b

    GYRO_CONFIG = 0x1B
    FS_250  = 0
    FS_500  = 1
    FS_1000 = 2
    FS_2000 = 3

    ACCEL_CONFIG = 0x1C
    AFS_2g  = 0
    AFS_4g  = 1
    AFS_8g  = 2
    AFS_16g = 3

    ORIENTATION = {
        'gyro_x': ('gyro_x', 1),
        'gyro_y': ('gyro_y', 1),
        'gyro_z': ('gyro_z', 1),
        'acc_x' : ('acc_x',  1),
        'acc_y' : ('acc_y',  1),
        'acc_z' : ('acc_z',  1)
    }

    ACCEL_SCALE = {
        AFS_2g  : [ 2, 16384.0],
        AFS_4g  : [ 4, 8192.0],
        AFS_8g  : [ 8, 4096.0],
        AFS_16g : [16, 2048.0]
        }

    TEMP_START_BLOCK  = 0x41
    GYRO_START_BLOCK  = 0x43
    ACCEL_START_BLOCK = 0x3B

    GYRO_SCALE = {
        FS_250  : [ 250, 131.0],
        FS_500  : [ 500, 65.5],
        FS_1000 : [1000, 32.8],
        FS_2000 : [2000, 16.4]
        }

    def __init__(self, pi, gpio, orient=ORIENTATION, address=0x69,
                 gyro_scale=FS_250, accel_scale=AFS_16g, bus=1
                 ):
        self.pi = pi
        self.bus = smbus.SMBus(1)

        self.address = address
        self.gpio = gpio
        self.gyro_scale = gyro_scale
        self.accel_scale = accel_scale

        self.orientation = orient

        # Enable output pin via pigpio
        self.pi.set_mode(self.gpio, pigpio.OUTPUT)

        # Set this sensor's address to 0x69 to distinguish it
        self.enable_sensor()
        # We need to wake up the module as it start in sleep mode
        self.bus.write_byte_data(self.address, MPU9250.PWR_MGMT_1, 0x00)
        # Set the gryo resolution
        self.bus.write_byte_data(
            self.address, MPU9250.GYRO_CONFIG, self.gyro_scale << 3
            )
        # Set the accelerometer resolution
        self.bus.write_byte_data(
            self.address, MPU9250.ACCEL_CONFIG, self.accel_scale << 3
            )
        # Set this sensor's address back to 0x68 with the others
        self.disable_sensor()


    def set_gyro_calibration(self,offsetx,offsety,offsetz):
        ''' Save gyro calibration values to (temporary) hardware registers '''
        self.enable_sensor()
        data = bytearray()
        data.append((offsetx >> 8) & 0xff)
        data.append((offsetx) & 0xff)
        data.append((offsety >> 8) & 0xff)
        data.append((offsety) & 0xff)
        data.append((offsetz >> 8) & 0xff)
        data.append((offsetz) & 0xff)
        self.bus.write_byte_data(self.address, 0x13, data[0])
        self.bus.write_byte_data(self.address, 0x14, data[1])
        self.bus.write_byte_data(self.address, 0x15, data[2])
        self.bus.write_byte_data(self.address, 0x16, data[3])
        self.bus.write_byte_data(self.address, 0x17, data[4])
        self.bus.write_byte_data(self.address, 0x18, data[5])
        self.disable_sensor()


    def set_accel_calibration(self,offsetx,offsety,offsetz):
        ''' Save accel calibration values to (temporary) hardware registers '''
        self.enable_sensor()
        data = bytearray()
        data.append((offsetx >> 8) & 0xff)
        data.append((offsetx) & 0xff)
        data.append((offsety >> 8) & 0xff)
        data.append((offsety) & 0xff)
        data.append((offsetz >> 8) & 0xff)
        data.append((offsetz) & 0xff)
        #ignore LSB to avoid overwriting temp bit
        self.bus.write_byte_data(self.address, 119, data[0])
        self.bus.write_byte_data(self.address, 122, data[2])
        self.bus.write_byte_data(self.address, 125, data[4])
        self.disable_sensor()

    def set_orientation(self, newOrientation):
        ''' Change the orientation for this specific sensor '''
        self.orientation = newOrientation

    def enable_sensor(self):
        ''' Pull this sensor's enable pin HIGH '''
        self.pi.write(self.gpio, 1)

    def disable_sensor(self):
        ''' Pull this sensor's enable pin LOW '''
        self.pi.write(self.gpio, 0)

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
        return raw_acc / MPU9250.ACCEL_SCALE[self.accel_scale][1]

    def scale_gyro(self, raw_gyro):
        ''' Convert raw gyro value to rad/s '''
        return raw_gyro / MPU9250.GYRO_SCALE[self.gyro_scale][1]

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
        try:
            self.refresh_data()
            # Convert axis and reverse signs if needed
            return {
                self.orientation['gyro_x'][0] : self.gyro_scaled_x * self.orientation['gyro_x'][1],
                self.orientation['gyro_y'][0] : self.gyro_scaled_y * self.orientation['gyro_y'][1],
                self.orientation['gyro_z'][0] : self.gyro_scaled_z * self.orientation['gyro_z'][1],
                self.orientation['acc_x'][0]  : self.accel_scaled_x * self.orientation['acc_x'][1],
                self.orientation['acc_y'][0]  : self.accel_scaled_y * self.orientation['acc_y'][1],
                self.orientation['acc_z'][0]  : self.accel_scaled_z * self.orientation['acc_z'][1]
            }
        except:
            # Catch any errors (intended for I/O but let's be extra safe here)
            return {
                'gyro_x' : 0.0,
                'gyro_y' : 0.0,
                'gyro_z' : 0.0,
                'acc_x'  : 0.0,
                'acc_y'  : 0.0,
                'acc_z'  : 0.0
            }

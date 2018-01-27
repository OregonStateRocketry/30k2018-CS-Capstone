from mpu6050.mpu6050.mpu6050 import mpu6050
from Adafruit_Python_BMP.Adafruit_BMP.BMP085 import BMP085
import time

def setup_mpu(mpu):
    ''' Configure default settings for the MPU6050 '''
    mpu.set_accel_range(0x18)   # Up to 16 g's
    mpu.set_gyro_range(0x10)    # Up to 1000 deg/sec
    # assert(mpu.read_accel_range(), 16)
    # assert(mpu.read_gyro_range(), 1000)
    return 1


def getLine(mpu):
    l = mpu.get_all_data()
    return (
        l[0]['x'], l[0]['y'], l[0]['z'],
        l[1]['x'], l[1]['y'], l[1]['z'],
        l[2]
    )


if __name__ == '__main__':
    mpu = mpu6050(0x68)
    setup_mpu(mpu)
    bmp = BMP085(address=0x77)

    with open('raw_data.txt', 'w') as f:
        # Give each new file a source and csv header
        f.write("Payload_Avionics\n")
        # f.write("{},{},{},{},{},{},{}\n".format(
        #     'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'temp'
        # ))
        f.write("{},{},{},{},{},{},{},{},{}, {}\n".format(
            'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mpu_temp',
            'bmp_temp', 'bmp_pres', 'bmp_alt'
        ))
        # Debugging: find out how long it takes to log 1000 samples
        start_time = time.time() #seconds since epoch
        for i in range(1000):
            # acc, gyro, temp = mpu.get_all_data()
            f.write("{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f},{:.3f}\n".format(
                *mpu.get_all_data(), bmp.read_temperature(),
                bmp.read_pressure(), bmp.read_altitude()
            ))
        duration = time.time()-start_time
        print("Wrote 1000 lines in {:.4f} seconds.  ({:.4f} seconds per row.)".format(
            duration, duration/1000
        ))

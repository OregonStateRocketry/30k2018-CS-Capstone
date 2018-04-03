from smbus import SMBus
import time

I2C_ADDRESS         = 0x60
# Important registers
PT_DATA_CFG         = 0x13
CTRL_REG1           = 0x26
PRESSURE_REG        = 0x01  # MSB of 3-bit pressure sample
TEMPERATURE_REG     = 0x04  # MSB of 2-bit temperature sample

# Useful bit patterns
CTRL_128_REFRESH    = 0xBA  # ~3 Hz
CTRL_64_REFRESH     = 0xB2  # ~15 Hz
CTRL_8_REFRESH      = 0x9A  # ~38 Hz
CTRL_4_REFRESH      = 0x92  # ~67 Hz but noticeable loss of precision
DATA_CFG_USEFLAGS   = 0x07  # Use flags to signal ready/not ready samples

class MPL3115A2(object):
    def __init__(self):
        self._bus = SMBus(1)

        self._bus.write_byte_data(
            I2C_ADDRESS,
            PT_DATA_CFG,
            DATA_CFG_USEFLAGS)

        self._bus.write_byte_data(
            I2C_ADDRESS,
            CTRL_REG1,
            CTRL_8_REFRESH)

    def readTempAlt(self):
        # Read 5 bits that include 3-bit pressure and 2-bit temperature
        data = self._bus.read_i2c_block_data(I2C_ADDRESS, PRESSURE_REG, 5)
        # Instruct MPL to prepare the next sample
        self._bus.write_byte_data(
            I2C_ADDRESS,
            CTRL_REG1,
            CTRL_8_REFRESH)

        # Condense 3 bits of altitude and round to nearest meter
        # alt = int( ( (data[0] << 16) | (data[1] << 8) | data[2] ) / 65535 )
        # alt = (((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) / 16) / 16.0 * 3.28084
        alt = int(((data[0] * 65536) + (data[1] * 256) + (data[2] & 0xF0)) * 0.01281578125)
        # Condense 2 bits into temperature in C
        temp = ((data[3] * 256) + (data[4] & 0xF0)) / 256.0
        return temp, alt


# def demo(num):
#     mpl = MPL3115A2()
#     last_time = time.time()
#     now = time.time()
#     while num:
#         if num not True: num -= 1
#
#         p, t = mpl.readTempAlt()
#         now = time.time()
#         print(now - last_time, p, t)
#         last_time = now
#
# if __name__ == "__main__":
#     demo()

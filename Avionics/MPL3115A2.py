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
        self.last_alt = 0
        self.temp = 0
        self.offset = 0
        self.errortemp = 9999

    def readTempAlt(self):
        try:
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
            # Ignore altitude values outside some possible range
            if alt > 50000 or alt < 0:
                alt = self.last_alt
            self.last_alt = alt
            # Condense 2 bits into temperature in C
            self.temp = ((data[3] * 256) + (data[4] & 0xF0)) / 256.0
            return self.temp, (alt + self.offset)
        except:
            # Catch any errors (intended for I/O but let's be extra safe here)
            # Returning the last known value is the safest way to prevent
            # accidentally triggering the experiment phase
            # return an error temperature to switch to last phase if altimeter is in error
            return self.errortemp, self.last_alt


    def setOffset(self, realalt):
        t, a = self.readTempAlt()
        sleep(0.1)
        t, a = self.readTempAlt()
        self.offset = realalt - a

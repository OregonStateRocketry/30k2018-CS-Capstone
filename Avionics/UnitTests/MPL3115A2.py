from smbus import SMBus

#I2C ADDRESS/BITS

MPL3115A2_ADDRESS = (0x60)

#REGISTERS

MPL3115A2_REGISTER_STATUS = (0x00)
MPL3115A2_REGISTER_STATUS_TDR = 0x02
MPL3115A2_REGISTER_STATUS_PDR = 0x04
MPL3115A2_REGISTER_STATUS_PTDR = 0x08

MPL3115A2_REGISTER_PRESSURE_MSB = (0x01)
MPL3115A2_REGISTER_PRESSURE_CSB = (0x02)
MPL3115A2_REGISTER_PRESSURE_LSB = (0x03)

MPL3115A2_REGISTER_TEMP_MSB = (0x04)
MPL3115A2_REGISTER_TEMP_LSB = (0x05)

MPL3115A2_REGISTER_DR_STATUS = (0x06)

MPL3115A2_OUT_P_DELTA_MSB = (0x07)
MPL3115A2_OUT_P_DELTA_CSB = (0x08)
MPL3115A2_OUT_P_DELTA_LSB = (0x09)

MPL3115A2_OUT_T_DELTA_MSB = (0x0A)
MPL3115A2_OUT_T_DELTA_LSB = (0x0B)

MPL3115A2_BAR_IN_MSB = (0x14)

MPL3115A2_WHOAMI = (0x0C)

#BITS

MPL3115A2_PT_DATA_CFG = 0x13
MPL3115A2_PT_DATA_CFG_TDEFE = 0x01
MPL3115A2_PT_DATA_CFG_PDEFE = 0x02
MPL3115A2_PT_DATA_CFG_DREM = 0x04

MPL3115A2_CTRL_REG1 = (0x26)
MPL3115A2_CTRL_REG1_SBYB = 0x01
MPL3115A2_CTRL_REG1_OST = 0x02
MPL3115A2_CTRL_REG1_RST = 0x04
MPL3115A2_CTRL_REG1_OS1 = 0x00
MPL3115A2_CTRL_REG1_OS2 = 0x08
MPL3115A2_CTRL_REG1_OS4 = 0x10
MPL3115A2_CTRL_REG1_OS8 = 0x18
MPL3115A2_CTRL_REG1_OS16 = 0x20
MPL3115A2_CTRL_REG1_OS32 = 0x28
MPL3115A2_CTRL_REG1_OS64 = 0x30
MPL3115A2_CTRL_REG1_OS128 = 0x38
MPL3115A2_CTRL_REG1_RAW = 0x40
MPL3115A2_CTRL_REG1_ALT = 0x80
MPL3115A2_CTRL_REG1_BAR = 0x00
MPL3115A2_CTRL_REG2 = (0x27)
MPL3115A2_CTRL_REG3 = (0x28)
MPL3115A2_CTRL_REG4 = (0x29)
MPL3115A2_CTRL_REG5 = (0x2A)

MPL3115A2_REGISTER_STARTCONVERSION = (0x12)

class MPL3115A2(object):
    def __init__(self):
        self._bus = SMBus(1)
        self._whoami = self._bus.read_byte_data(MPL3115A2_ADDRESS, MPL3115A2_WHOAMI)
        if self._whoami != 0xc4:
            print("Device not active")

        self._bus.write_byte_data(
            MPL3115A2_ADDRESS,
            MPL3115A2_PT_DATA_CFG,
            MPL3115A2_PT_DATA_CFG_TDEFE |
            MPL3115A2_PT_DATA_CFG_PDEFE |
            MPL3115A2_PT_DATA_CFG_DREM)

        #These set the sample rate to be very fast and allow for us to constantly sample without needing it to be ready for a sample.
        self._bus.write_byte_data(
                MPL3115A2_ADDRESS,
                MPL3115A2_CTRL_REG1,
                0b00011011)
        self._bus.write_byte_data(
                MPL3115A2_ADDRESS,
                MPL3115A2_CTRL_REG1,
                0b00011001)


    def temperature(self):
        msb, lsb = self._bus.read_i2c_block_data(MPL3115A2_ADDRESS,MPL3115A2_REGISTER_TEMP_MSB,2)
        #print(msb, lsb)
        return msb + (lsb >> 4)/16.0


    def pressure(self):
        msb, csb, lsb = self._bus.read_i2c_block_data(MPL3115A2_ADDRESS,MPL3115A2_REGISTER_PRESSURE_MSB,3)
        #print(msb, csb, lsb)
        return ((msb * 65536) + (csb * 256) + (lsb & 0xF0))/ 64
    def update(self): #preps for next check
        # MPL3115A2 address, 0x60(96)
        # Select data configuration register, 0x13(19)
        #		0x07(07)	Data ready event enabled for altitude, pressure, temperature
        #self._bus.write_byte_data(0x60, 0x13, 0x07)
        # MPL3115A2 address, 0x60(96)
        # Select control register, 0x26(38)
        #		0x39(57)	Active mode, OSR = 128, Barometer mode
        self._bus.write_byte_data(
        MPL3115A2_ADDRESS,
        MPL3115A2_CTRL_REG1,
        0b00011011)
        self._bus.write_byte_data(
        MPL3115A2_ADDRESS,
        MPL3115A2_CTRL_REG1,
        0b00011001)

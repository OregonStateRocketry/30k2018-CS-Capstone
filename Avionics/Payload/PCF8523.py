from smbus import SMBus
import math
import time
import sys

def _bcd2bin(value):
    """Convert binary coded decimal to Binary

    Arguments:
    value - the BCD value to convert to binary (required, no default)
    """
    return value - 6 * (value >> 4)

def _bin2bcd(value):
    """Convert a binary value to binary coded decimal.

    Arguments:
    value - the binary value to convert to BCD. (required, no default)
    """
    return value + 6 * (value // 10)

class PCF8523:
    def __init__(self):
        self._bus = SMBus(1)

    def gettime(self):
        (secs, mins, hours, days, wkday, mnth, yr) = self._bus.read_i2c_block_data(0x68,0x03,7)
        yr = _bcd2bin(yr) + 2000
        mnth = _bcd2bin(mnth)
        wkday = _bcd2bin(wkday)
        days = _bcd2bin(days)
        hours = _bcd2bin(hours)
        mins = _bcd2bin(mins)
        secs = _bcd2bin(secs & 0x7F)
        return time.struct_time([yr, mnth, days, hours, mins, secs, wkday, 1, -1])

    def settime(self, value):
        buff = [_bin2bcd(value.tm_sec) &0x7F,
                _bin2bcd(value.tm_min),
                _bin2bcd(value.tm_hour),
                _bin2bcd(value.tm_mday),
                _bin2bcd(value.tm_wday),
                _bin2bcd(value.tm_mon),
                _bin2bcd(value.tm_year - 2000)]
        self._bus.write_i2c_block_data(0x68,0x03,buff)
        return True

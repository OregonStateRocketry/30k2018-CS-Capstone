from subprocess import Popen, PIPE
import re
# Inspired by http://alloutput.com/amateur-radio/aprs-notes/

class DWParser:
    ''' Manage collecting and parsing audio signals with Direwolf '''

    def __init__(self):
        ''' Constructor
        Defaults to Direwolf settings for Enhanced Plus mode and 2x sampling,
        which yielded the best results during tests.
        '''
        self.dw = None
        self.dw = Popen(
            ['direwolf', '-P', 'E+', '-D', '2'],
            stdout=PIPE
            )
        for line in self.dw.stdout:
            if b'Ready' in line:
                break
            elif b'Pointless to continue' in line:
                # print("DWParser could not open audio device, reboot.")
                raise EnvironmentError('Unable to open audio device')
        self.count = 0

    def __del__(self):
        ''' De-Constructor '''
        if self.dw:
            self.dw.kill()

    def convertDMtoDD(self, d, m):
        ''' Convert GPS DD MM.MMMM to DD.DDDD which is easier to use'''
        return round(d + m/60.0, 4)

    def checkAudio(self):
        ''' Hangs until it parses one line from Direwolf '''
        ''' TODO: Rewrite so that it does not hang! (Or at least updates db) '''
        data = {}
        while len(data) < 6:
            # In python2 stdout is a string, in python3 it's bytecode
            line = self.dw.stdout.readline().decode('utf-8')
            if 'audio level' in line:
                # AG7IU-1 audio level = 21(10/5)   [NONE]   __|||||||
                data['callsign'] = line.split()[0]          # AG7IU-1
                data['audio level'] = int(re.findall(r' = ([0-9]*)', line)[0]) # 21
            else:
                # [1;32m[5;47m[0.5] AG7IU-1>APBL10:!4533.17N/12246.66WA/A=001105F
                # [1;34m[5;47mPosition, Aid station, BigRedBee BeeLine
                # [1;34m[5;47mN 45 33.1700, W 122 46.6600, alt 1105 ft
                l = re.findall(r'.*N ([0-9]*) ([0-9]*.[0-9]*), W ([0-9]*) ([0-9]*.[0-9]*), alt ([0-9]*) (\w+)', line)
                if l != [] and len(l[0]) == 6:
                    l = l[0]
                    data['lat'] = self.convertDMtoDD(int(l[0]), float(l[1]))
                    data['lon'] = self.convertDMtoDD(int(l[2]), float(l[3]))
                    data['alt'] = int(l[4])
                    data['alt units'] = l[5]
        self.count += 1
        return data

# def demo():
#     print("Connecting to direwolf audio parser...", end='', flush=True)
#     wolf = None
#     try:
#         wolf = DWParser()
#     except Exception as e:
#         print(" FAILED")
#         print("Direwolf failed to start, often solved by rebooting.")
#         print("Debugging info: ",e)
#         sys.exit(0)
#     print(" OK")
#
#     while(True):
#         print("Waiting for a packet..")
#         print(wolf.checkAudio())
#
# if __name__ == '__main__':
#     demo()

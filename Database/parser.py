import sys, os.path
from Mariadb import Mariadb
from DWParser import DWParser
import datetime
import fileinput

class Parser:
    ''' A class representing each Parser '''

    def __init__(self, dbConfig='config.yml', log='plog.csv', fid=None):
        self.db = self.connectDB(dbConfig)
        self.callsign = 'UNKNOWN'
        self.logFile = log

        # Find the active flight, and serial number for this parser
        self.f_id = fid or self.connectParser(fid)

        # Prepare the direwolf client
        self.wolf = self.connectDirewolf()


    def connectDB(self, cf):
        # Connect to the ESRA database
        print("Connecting to database...", end='', flush=True)
        db = None
        try:
            db = Mariadb(configFile=cf)
        except Exception as e:
            print(" FAILED")
            print("Start the ESRA database before running this program.")
            print("Debugging info: ",e)
            sys.exit(0)
        print(" OK")
        return db


    def connectDirewolf(self):
        # Begin Direwolf monitor
        print("Connecting to direwolf audio parser...", end='', flush=True)
        wolf = None
        try:
            wolf = DWParser()
        except Exception as e:
            print(" FAILED")
            print("Direwolf failed to start, often solved by rebooting.")
            print("Debugging info: ",e)
            sys.exit(0)
        print(" OK")
        return wolf


    def connectParser(self, fid=None):
        # Check status and display parser info
        self.f_id = fid or self.db.checkActiveFlight()
        while not self.f_id:
            # f_id == None means no active flights, let's try to fix that:
            self.db.addNewFlight()
            self.f_id = self.db.checkActiveFlight()

        self.serialNum = self.getSerial()
        self.db.registerParser(self.serialNum)

        print("Parser Serial #: {}.".format(self.serialNum))
        print("The current flight ID is: {}.".format(self.f_id))
        return self.f_id


    def insertBeelineGPS(self, data):
        self.db.validateCallsign(data['callsign'])
        print("data = ", data)
        return self.db.insertRow(
            table='BeelineGPS',
            cols='f_id, lat, lon, alt, p_id, c_id',
            vals=["""
                {f_id}, {lat}, {lon}, {alt},
                (SELECT id FROM Parser_Status WHERE serialNum='{serialNum}'),
                (SELECT id FROM Callsigns WHERE callsign='{callsign}')
                """.format(**data)
            ]
        )


    def getSerial(self):
        ''' Read the serial number for the current pi '''
        try:
            with open('/proc/cpuinfo','r') as f:
                return f.readlines()[-1].split()[-1]
        except:
                return '0000'


    def createBeelineLog(self, filename):
        # Create log file if not exists
        try:
            f = open(filename, 'r')
            f.close()
        except IOError:
            f = open(filename, 'w')
            f.write('BeelineGPS\n')
            # Write header to log
            f.write('timestamp,callsign,audio level,lat,lon,alt,' +
                    'alt units,f_id,serialNum\n')
            f.close()


    def listen(self, numLoops=True):
        # Ensure we have a few necessary things
        assert(self.f_id)
        assert(self.serialNum)
        assert(self.callsign)
        print("\nListening for packets...")
        # Ensure the log file exists and is ready
        self.createBeelineLog(self.logFile)
        with open(self.logFile, 'a+') as log:
            while (numLoops):
                if (numLoops is not True): numLoops -= 1
                if (datetime.datetime.now() - self.db.last_connected).total_seconds() > 3:
                    self.db.updateParserTable(
                        self.f_id, self.serialNum, self.callsign
                        )
                # Needs to be improved so this doesn't hang..
                data = self.wolf.checkAudio()
                data['f_id'] = self.f_id
                data['serialNum'] = self.serialNum
                #print("Debugging: data = ",data)
                self.insertBeelineGPS(data)     # write to database
                log.write(
                    str(datetime.datetime.now())+','+   \
                    ','.join([str(value) for key, value in data.items()])+'\n'
                    ) # write values to local log
        return True


if __name__ == "__main__":
    print("ESRA 30k Telemetry Parser.")
    if len(sys.argv) > 1:
        client = Parser(dbConfig=sys.argv[1])
    else:
        client = Parser()

    client.listen()

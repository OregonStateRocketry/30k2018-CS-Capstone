import pymysql.cursors
import datetime

class mariadb:
    '''A class to interact with the ESRA mariadb database'''

    def __init__(self):
        with open('config.yml', 'r') as cf:
            cf = yaml.load(cf)
            user=cf['database']['user']
            password=cf['database']['pass']
        self.connection = pymysql.connect(
            host='esra.local',
            user=user,
            password=password,
            db='esra',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.last_connected = datetime.datetime(2000, 1, 1, 00, 00)
        self.f_id = self.checkActiveFlight()
        self.parser_serial = self.getParserSerial()
        self.registerParser()
        # self.status = 'Idle'
        self.callsign = 'UNKNOWN'

    def getParserSerial(self):
        ''' Read the serial number for the current pi'''
        try:
            with open('/proc/cpuinfo','r') as f:
                return f.readlines()[-1].split()[-1]
        except:
            return '0000'

    def registerParser(self):
        ''' Ensure this serial number is in Parser_Status '''
        with self.connection.cursor() as c:
            return c.execute(
                """
                    INSERT INTO Parser_Status(parser_id, last_activity)
                    VALUES('{}', NOW())
                    ON DUPLICATE KEY UPDATE last_activity=NOW()
                """.format(self.parser_serial)
            )

    def checkActiveFlight(self):
        '''Returns the currently active flight number, if available'''
        with self.connection.cursor() as c:
            sql = """
                SELECT flight_id from Flights
                where status = 'Active'
                ORDER BY start_timestamp asc
            """
            c.execute(sql)
            return c.fetchone()['flight_id']

    def updateParserTable(self):
        '''Updates the Parser_Status table with diagnostic info'''
        self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            return c.execute("""
                UPDATE Parser_Status SET
                using_f_id='{fid}',
                last_activity=NOW(),
                callsign='{cs}'
                WHERE parser_id='{ser}'
            """.format(
                    fid=self.f_id,
                    cs=self.callsign,
                    ser=self.parser_serial
                )
            )

if __name__ == "__main__":
    db = mariadb()
    print("ESRA 30k Rocket Parser program running...")
    print("Parser Serial #: {}.".format(db.parser_serial))
    print("The current flight is: {}.".format(db.f_id))
    while True:
        if (datetime.datetime.now() - db.last_connected).total_seconds() > 3:
            db.updateParserTable()
        # Try to parse an incoming string here

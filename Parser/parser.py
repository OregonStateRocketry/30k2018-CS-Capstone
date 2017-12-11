import pymysql.cursors
import datetime

class mariadb:
    '''A class to interact with the ESRA mariadb database'''

    def __init__(self):
        self.connection = pymysql.connect(
            host='esra.local',
            user='levi',
            password='esra18',
            db='esra',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        self.last_connected = datetime.datetime(2000, 1, 1, 00, 00)
        self.f_id = self.checkActiveFlight()
        self.parser_serial = self.getParserSerial()
        self.status = 'Idle'

    def getParserSerial(self):
        ''' Read the serial number for the current pi'''
        try:
            with open('/proc/cpuinfo','r') as f:
                return f.readlines()[-1].split()[-1]
        except:
            return '0000'

    def doSelect(self, table, fields):
        ''' SELECT some fields from some table'''
        with self.connection.cursor() as c:
            sql = "SELECT {} FROM {}".format(fields, table)
            c.execute(sql)
            return c.fetchall()

    def doInsert(self, table, fields, values):
        '''INSERT a list of values into some fields in some table'''
        with self.connection.cursor() as c:
            sql = "INSERT INTO {}({}) VALUES({})".format(table, fields, values)
            return c.execute(sql)

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
                REPLACE INTO Parser_Status (parser_id, using_f_id, last_activity, status)
                VALUES('{}', '{}', NOW(), '{}')
                """.format(self.parser_serial, self.f_id, self.status)
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

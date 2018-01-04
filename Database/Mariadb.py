import pymysql.cursors
import datetime
import yaml

class Mariadb:
    '''A class to interact with the ESRA mariadb database'''

    def __init__(self):
        with open('config.yml', 'r') as cf:
            cf = yaml.load(cf)
        self.connection = pymysql.connect(
            host        =   cf['database']['host'],
            user        =   cf['database']['user'],
            password    =   cf['database']['pass'],
            db          =   cf['database']['db'],
            charset     =   'utf8mb4',
            cursorclass =   pymysql.cursors.DictCursor,
            autocommit  =   True
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


    def getCurrentPosition(self):
        ''' Returns info about the current location of the flight '''
        with self.connection.cursor() as c:
            sql = """
                SELECT B.*
                    FROM Flights AS F
                INNER JOIN BeelineGPS AS B
                    ON B.f_id = F.flight_id
                INNER JOIN (
                    SELECT callsign, MAX(time) AS latest
                    FROM BeelineGPS
                    GROUP BY callsign
                ) AS M
                ON M.callsign = B.callsign AND M.latest = B.time
                WHERE F.status = 'Active'
            """
            c.execute(sql)
            return c.fetchall()


    def getDBTime(self):
        ''' Returns the current time on the database '''
        with self.connection.cursor() as c:
            sql = "SELECT NOW()"
            c.execute(sql)
            return c.fetchone()['NOW()']


    def getParserTable(self):
        ''' Returns the Parser_Status table from the database '''
        # self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            sql = "SELECT * from Parser_Status"
            c.execute(sql)
            return c.fetchall()


    def registerParser(self, parser_serial):
        ''' Ensure this serial number is in Parser_Status '''
        # self.parser_serial = parser_serial
        with self.connection.cursor() as c:
            return c.execute(
                """
                    INSERT INTO Parser_Status(parser_id, last_activity)
                    VALUES('{}', NOW())
                    ON DUPLICATE KEY UPDATE last_activity=NOW()
                """.format(parser_serial)
            )


    def updateParserTable(self, f_id, parser_serial, callsign):
        '''Updates the Parser_Status table with diagnostic info'''
        # self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            return c.execute("""
                UPDATE Parser_Status SET
                using_f_id='{fid}',
                last_activity=NOW(),
                callsign='{cs}'
                WHERE parser_id='{ser}'
            """.format(
                    fid=f_id,
                    cs=callsign,
                    ser=parser_serial
                )
            )

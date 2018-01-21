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
        self.last_connected = None


    def checkActiveFlight(self):
        ''' Returns the currently active flight number, if available '''
        with self.connection.cursor() as c:
            sql = """
                SELECT flight_id FROM Flights
                WHERE status = 'Active'
                ORDER BY start_timestamp DESC
                LIMIT 1
            """
            c.execute(sql)
            res = c.fetchone()
            return res['flight_id'] if res else None;

    def getMaxFlightID(self):
        ''' Returns the largest flight_id number '''
        with self.connection.cursor() as c:
            sql = 'SELECT MAX(flight_id) FROM Flights'
            c.execute(sql)
            return c.fetchone()['MAX(flight_id)']


    def createNewActiveFlight(self, fid):
        ''' Create a new flight ID while limiting duplicates '''
        with self.connection.cursor() as c:
            sql = """
                INSERT INTO Flights(flight_id, start_timestamp, status)
                VALUES({}, NOW(), 'Active')
            """.format(fid)
            return c.execute(sql)


    def getFlightTable(self):
        ''' Returns the Flight table '''
        with self.connection.cursor() as c:
            c.execute("SELECT * FROM Flights")
            return c.fetchall()


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


    def insertRow(self, table, cols, vals):
        ''' Inserts a single row into the database '''
        with self.connection.cursor() as c:
            sql = """
                INSERT INTO {table}( {cols} ) VALUES
                """.format(table=table, cols=cols)
            for v in vals:
                sql += '({}),'.format(v)
            # Erase the trailing comma
            sql = sql[:-1]
            return c.execute(sql)


    def getParserTable(self):
        ''' Returns the Parser_Status table from the database '''
        # self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            sql = "SELECT * FROM Parser_Status"
            c.execute(sql)
            return c.fetchall()


    def registerParser(self, parser_serial):
        ''' Ensure this serial number is in Parser_Status '''
        self.last_connected = datetime.datetime.now()
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
        self.last_connected = datetime.datetime.now()
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

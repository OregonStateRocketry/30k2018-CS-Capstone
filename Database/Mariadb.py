import pymysql.cursors
import datetime
import yaml
from os import system

class Mariadb:
    '''A class to interact with the ESRA mariadb database'''

    def __init__(self, configFile='config.yml'):
        assert(configFile)  # ensure we have a config file

        try:
            with open(configFile, 'r') as cf:
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
        except Exception as e:
            raise EnvironmentError

        self.cf = cf
        self.last_connected = None
        self.valid_callsigns = {}


    def importSQLFile(self, sqlFile):
        ''' Attempt to import an entire SQL file, mostly for testing '''
        cmd = "mysql -h {host} -u {user} -p{pw} {db} < {sqlFile}".format(
            host = self.cf['database']['host'],
            user = self.cf['database']['user'],
            pw   = self.cf['database']['pass'],
            db   = self.cf['database']['db'],
            sqlFile = sqlFile
        )
        return system(cmd)


    def addNewFlight(self):
        ''' Attempt to create a new flight without duplicates '''
        new_fid = (self.getMaxFlightID() or 0) + 1
        return self.createNewActiveFlight(new_fid)


    def checkActiveFlight(self):
        ''' Returns the currently active flight number, if available '''
        with self.connection.cursor() as c:
            sql = """
                SELECT id FROM Flights
                WHERE status = 'Active'
                LIMIT 1
            """
            c.execute(sql)
            res = c.fetchone()
            return res['id'] if res else None;


    def createNewActiveFlight(self, fid):
        ''' Create a new flight ID while limiting duplicates '''
        with self.connection.cursor() as c:
            sql = """
                INSERT INTO Flights(id, status)
                VALUES({}, 'Active')
            """.format(fid)
            c.execute(sql)
            return c.lastrowid


    def getCurrentPosition(self):
        ''' Returns info about the current location of the flight '''
        with self.connection.cursor() as c:
            sql = """
            SELECT B.latest, B.lat, B.lon, B.alt, C.callsign FROM Flights AS F
            JOIN (
                SELECT f_id, c_id, lat, lon, alt, MAX(time) AS latest
                FROM BeelineGPS
                GROUP BY f_id, c_id
            ) B ON B.f_id = F.id
            JOIN ( SELECT id, callsign FROM Callsigns ) C ON C.id = B.c_id
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


    def getFlightTable(self):
        ''' Returns the Flight table '''
        with self.connection.cursor() as c:
            c.execute("SELECT * FROM Flights")
            return c.fetchall()


    def getMaxFlightID(self):
        ''' Returns the largest id number '''
        with self.connection.cursor() as c:
            sql = 'SELECT MAX(id) FROM Flights'
            c.execute(sql)
            return c.fetchone()['MAX(id)']


    def getParserTable(self):
        ''' Returns the Parser_Status table from the database '''
        # self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            sql = "SELECT * FROM Parser_Status"
            c.execute(sql)
            return c.fetchall()


    def validateCallsign(self, callsign):
        ''' Ensure a callsign already exists in the database '''
        # Return database id number of callsign, if known
        if callsign in self.valid_callsigns:
            return self.valid_callsigns[callsign]

        with self.connection.cursor() as c:
            # Query and store database id number for callsign
            sql = """
                SELECT id FROM Callsigns WHERE callsign='{}'
                """.format(callsign)
            c.execute(sql)
            result = c.fetchone()
            if result:
                self.valid_callsigns[callsign] = result
                return self.valid_callsigns[callsign]

            # Insert and store database id number for callsign
            sql = """
                INSERT IGNORE INTO Callsigns(callsign) VALUES('{}')
                """.format(callsign)
            c.execute(sql)
            self.valid_callsigns[callsign] = c.lastrowid
            return self.valid_callsigns[callsign]


    def insertRow(self, table, cols, vals):
        ''' Inserts a single row into the database '''
        with self.connection.cursor() as c:
            sql = """
                INSERT INTO {table}( {cols} ) VALUES (
                """.format(table=table, cols=cols)
            for v in vals:
                sql += '{},'.format(v)
            # Erase the trailing comma
            sql = sql[:-1] + ')'
            c.execute(sql)
            return c.lastrowid


    def insertManyRows(self, table, cols, vals):
        ''' Inserts many rows into the same table and columns '''
        with self.connection.cursor() as c:
            sql = "INSERT INTO {} ({}) VALUES ({}%s)".format(
                table, cols, "%s, "*(len(vals[0])-1)
            )
            print('sql=', sql)
            print('\nvals=', vals)
            print("num cols = ", len(cols.split(',')) )
            print("num vals = ", len(vals[0]) )
            return c.executemany(sql, vals)


    def registerParser(self, parser_serial):
        ''' Ensure this serial number is in Parser_Status '''
        self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            c.execute(
                """
                    INSERT INTO Parser_Status(serialNum, last_activity)
                    VALUES('{}', NOW())
                    ON DUPLICATE KEY UPDATE last_activity=NOW()
                """.format(parser_serial)
            )
            return c.lastrowid


    def fetchSql(self, sql):
        ''' Run an SQL query and return the results '''
        with self.connection.cursor() as c:
            c.execute(sql)
            return c.fetchall()


    def updateParserTable(self, f_id, serialNum, callsign):
        '''Updates the Parser_Status table with diagnostic info'''
        self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            sql = """
                UPDATE Parser_Status SET
                using_f_id='{fid}',
                last_activity=NOW(),
                callsign='{cs}'
                WHERE serialNum='{ser}'
            """.format(fid=f_id, cs=callsign, ser=serialNum)
            c.execute(sql)
            return c.lastrowid

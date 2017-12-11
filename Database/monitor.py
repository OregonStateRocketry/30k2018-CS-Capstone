import pymysql.cursors
import datetime
import curses
from curses import wrapper

class mariadb:
    '''A class to interact with the ESRA mariadb database '''

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

    def getParserSerial(self):
        ''' Read the serial number for the current pi '''
        try:
            with open('/proc/cpuinfo','r') as f:
                return f.readlines()[-1].split()[-1]
        except:
            return '0000'

    def doSelect(self, table, fields):
        ''' SELECT some fields from some table '''
        with self.connection.cursor() as c:
            sql = "SELECT {} FROM {}".format(fields, table)
            c.execute(sql)
            return c.fetchall()

    def getActiveFlights(self):
        '''Returns the currently active flight, if available '''
        with self.connection.cursor() as c:
            sql = """
                SELECT * from Flights
                where status = 'Active'
                ORDER BY start_timestamp desc
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
        self.last_connected = datetime.datetime.now()
        with self.connection.cursor() as c:
            sql = "SELECT * from Parser_Status"
            c.execute(sql)
            return c.fetchall()

def main(stdscr):
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.clear()
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    global screen
    screen = stdscr.subwin(23,99,0,0)
    screen.box()
    stdscr.addstr(1,1,"ESRA 30k Rocket Database Maintenance")
    stdscr.addstr(2,1,"Connecting to database . . ["),
    db = mariadb()
    stdscr.addstr(2,30,"OK",curses.color_pair(2))
    stdscr.addstr(2,33,"]")
    screen.refresh()

    stdscr.addstr(5,1,"Current parser table:")
    stdscr.addstr(6,1,"{:10}|{:10}|{:10}|{:20}".format(
        "Parser ID","Flight ID","Status","Last Activity"
    ))

    stdscr.addstr(15,1,"Currently active flights:")
    stdscr.addstr(16,1,"{:10}|{:20}|{:20}|{:15}|{:15}|{:10}".format(
        "Flight ID","Start Time","Last Activity",
        "Launch Lat", "Launch Lon", "Max Alt",
    ))
    while True:
        # No need to hammer the database, just check once per second
        if (datetime.datetime.now() - db.last_connected).total_seconds() >= 1:
            
            # Show the status of the various parsers
            rows = db.getParserTable()
            for i,r in enumerate(rows):
                stdscr.addstr(7+i,1,"{:10}|{:10}|{:10}|{:20}".format(
                    str(r['parser_id']),
                    str(r['using_f_id']),
                    '',
                    str(r['last_activity'])
                ))
                # Find out when the parsers last connected and colorize status
                parser_last_connected = (
                    db.getDBTime() - r['last_activity']
                ).total_seconds()
                if parser_last_connected < 5:
                    stdscr.addstr(7+i,24,r['status'],curses.color_pair(2))
                elif parser_last_connected < 30:
                    stdscr.addstr(7+i,24,r['status'],curses.color_pair(3))
                else:
                    stdscr.addstr(7+i,24,'DISC',curses.color_pair(4))

            # Show any currently active flights
            rows = db.getActiveFlights()
            for i,r in enumerate(rows):
                stdscr.addstr(17+i,1,
                    "{:10}|{:20}|{:20}|{:15}|{:15}|{:10}".format(
                    str(r['flight_id']),
                    str(r['start_timestamp']),
                    str(r['last_timestamp']),
                    r['launch_lat'],
                    r['launch_lon'],
                    str(r['max_alt'])
                ))
            db.getDBTime();
            screen.refresh()

if __name__ == "__main__":
    wrapper(main)

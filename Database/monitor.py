import pymysql.cursors
import datetime
import curses
import yaml
from curses import wrapper

class mariadb:
    '''A class to interact with the ESRA mariadb database '''

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

    def getParserSerial(self):
        ''' Read the serial number for the current pi '''
        try:
            with open('/proc/cpuinfo','r') as f:
                return f.readlines()[-1].split()[-1]
        except:
            return '0000'

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
    screen = stdscr.subwin(20,40,0,0)
    screen.box()
    stdscr.addstr(0,1,"ESRA 30k Rocket Summary")
    stdscr.addstr(1,1,". . . . . . . . . . . . . . . . .")
    stdscr.addstr(1,1,"Database status"),
    try:
        db = mariadb()
        stdscr.addstr(1,33,"[")
        stdscr.addstr(1,35,"OK",curses.color_pair(2))
        stdscr.addstr(1,38,"]")
    except:
        stdscr.addstr(1,33,"[")
        stdscr.addstr(1,35,"ERR",curses.color_pair(4))
        stdscr.addstr(1,38,"]")
    screen.refresh()

    # stdscr.addstr(3,1,"Parser status table:")
    stdscr.addstr(4,1,"{:6}{:3}{:7}{:6}{:10}".format(
        "PID", "F", "Status", "Delay", "Callsign"
    ))

    # stdscr.addstr(10,1,"Currently active flights:")
    stdscr.addstr(11,1,"{:3}{:6}{:7}{:8}{:7}{:6}".format(
        "F", "Delay", "Lat", "Lon", "Alt", "CS",
    ))

    db = None
    while not db:
        try:
            db = mariadb()
            stdscr.addstr(1,33,"[")
            stdscr.addstr(1,35,"OK",curses.color_pair(2))
            stdscr.addstr(1,38,"]")
        except:
            stdscr.addstr(1,33,"[")
            stdscr.addstr(1,35,"ERR",curses.color_pair(4))
            stdscr.addstr(1,38,"]")
        screen.refresh()

    while True:
        # No need to hammer the database, just check once per second
        if (datetime.datetime.now() - db.last_connected).total_seconds() >= 1:

            # Show the status of the various parsers
            rows = db.getParserTable()
            dbtime = db.getDBTime()
            for i,r in enumerate(rows):
                # Find out when the parsers last connected (in seconds)
                parser_last_connected = int(
                    (dbtime - r['last_activity']).total_seconds()
                )

                stdscr.addstr(5+i,1,"{:6}{:3}{:7}{:6}{:10}".format(
                    str(r['parser_id'])[-5:],
                    str(r['using_f_id']),
                    '',
                    str(parser_last_connected),
                    str(r['callsign'])
                ))
                if parser_last_connected < 10:
                    stdscr.addstr(5+i,10,'OK',curses.color_pair(2))
                elif parser_last_connected < 30:
                    stdscr.addstr(5+i,10,'SLOW',curses.color_pair(3))
                else:
                    stdscr.addstr(5+i,10,'DISC',curses.color_pair(4))

            # Show any currently active flights
            rows = db.getCurrentPosition()
            for i,r in enumerate(rows):
                delay = int(
                    (dbtime - r['time']).total_seconds()
                )
                stdscr.addstr(12+i,1,
                    "{:3}{:6}{:7}{:8}{:7}{:6}".format(
                    str(r['f_id']),
                    str(delay),
                    str(r['lat']),
                    str(r['lon']),
                    str(r['alt']),
                    r['callsign']
                ))
            db.getDBTime();
            screen.refresh()

if __name__ == "__main__":
    mariadb()
    wrapper(main)

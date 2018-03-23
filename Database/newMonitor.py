from Mariadb import Mariadb
import datetime
import time
import curses
from curses import wrapper

class Monitor:
    ''' Display summary on the ground station LCD screen '''

    def __init__(self, dbConfig='config.yml'):
        self.stdscr = curses.initscr()
        curses.noecho()
        # stdscr.clear()
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        self.screen = stdscr.subwin(20,40,0,0)
        screen.box()
        displayStaticElements(stdscr)

        self.db = connectToDatabase()

    def connectToDatabase():
        db = None
        stdscr.addstr(1,33,"[    ]")
        while not db:
            try:
                db = Mariadb(dbConfig)
                stdscr.addstr(1,35,"OK",curses.color_pair(2))
                screen.refresh()
            except Exception as e:
                stdscr.addstr(2,1,str(e))
                stdscr.addstr(1,35,"ERR",curses.color_pair(4))
                screen.refresh()
                time.sleep(5)
        return db

    def displayStaticElements(stdscr):
        ''' Runs once to display the static screen elements '''
        stdscr.addstr(0,1,"ESRA 30k Rocket Summary")
        stdscr.addstr(1,1,"Database status . . . . . . . . .")

        # stdscr.addstr(3,1,"Parser status table:")
        stdscr.addstr(4,1,"{:6}{:3}{:7}{:6}{:10}".format(
            "PID", "F", "Status", "Delay", "Callsign"
        ))

        # stdscr.addstr(10,1,"Currently active flights:")
        stdscr.addstr(11,1,"{:3}{:6}{:7}{:8}{:7}{:6}".format(
            "F", "Delay", "Lat", "Lon", "Alt", "CS",
        ))

    def updateParserSection(stdscr, db, dbtime):
        ''' Updates the section displaying parser statuses '''
        rows = db.getParserTable()
        for i,r in enumerate(rows):
            # Find out when the parsers last connected (in seconds)
            delay = int(
                (dbtime - r['last_activity']).total_seconds()
            )

            stdscr.addstr(5+i,1,"{:6}{:3}{:7}{:6}{:10}".format(
                str(r['parser_id'])[-5:],
                str(r['using_f_id']),
                '',
                str(delay) if delay < 600 else '>600',
                str(r['callsign'])
            ))
            if delay < 10:
                stdscr.addstr(5+i,10,'OK',curses.color_pair(2))
            elif delay < 30:
                stdscr.addstr(5+i,10,'SLOW',curses.color_pair(3))
            else:
                stdscr.addstr(5+i,10,'DISC',curses.color_pair(4))

    def updateLocationSection(stdscr, db, dbtime):
        ''' Updates the section displaying last known positions '''
        rows = db.getCurrentPosition()
        for i,r in enumerate(rows):
            delay = int(
                (dbtime - r['time']).total_seconds()
            )

            stdscr.addstr(12+i,1,
                "{:3}{:6}{:7}{:8}{:7}{:6}".format(
                str(r['f_id']),
                str(delay) if delay < 600 else '>600',
                str(r['lat'])[:6],
                str(r['lon'])[:7],
                str(r['alt'])[:6],
                r['callsign']
            ))

def main(stdscr, dbConfig):
    disp = Monitor(dbConfig)

    while True:
        dbtime = disp.db.getDBTime()
        # Update each of the display sections on the page
        updateParserSection(stdscr, db, dbtime)
        updateLocationSection(stdscr, db, dbtime)
        # Refresh the screen to apply new text
        screen.refresh()
        # No need to hammer the database, just check every other second
        time.sleep(2)


if __name__ == "__main__":
    wrapper(main, dbConfig='config.yml')

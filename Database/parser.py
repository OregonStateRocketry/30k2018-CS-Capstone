import sys, os.path
from Mariadb import Mariadb
from DWParser import DWParser
import datetime
import fileinput

def displayImportMenu(flights):
    validFlightIDs = []
    print("{:5}{:20}{:10}{}".format(
        'ID','Start Date','Duration','Max Alt'
        ))
    for f in flights:
        validFlightIDs.append(str(f['flight_id']))
        print("{:<5}{:20}{:10}{}".format(
            f['flight_id'],
            f['start_timestamp'].strftime('%Y-%m-%d %H:%M'),
            (f['last_timestamp']-f['start_timestamp']).strftime(
                '%H:%M:%S') if f['last_timestamp'] else 'Active',
            f['max_alt']
        ))
    return validFlightIDs

# def insertBeelineGPS(data)
#     t, lat, lon, alt, cs = line.split(',')
#     db.insertRow(
#         table='BeelineGPS',
#         cols='f_id, time, lat, lon, alt, callsign',
#         vals=["""{f_id}, STR_TO_DATE('{timestamp}', '%Y-%m-%d %H:%i:%s'),
#             {lat}, {lon}, {alt}, '{cs}'""".format(
#                 f_id=f_id, timestamp=t, lat=lat, lon=lon, alt=alt, cs=cs
#             )
#         ]
#     )

def insertBeelineGPS(db, f_id, data):
    data['f_id'] = f_id
    data['timestamp'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%s.%f')[:-4]
    print('Inserting ', data)
    db.insertRow(
        table='BeelineGPS',
        cols='f_id, time, lat, lon, alt, callsign',
        vals=["""{f_id}, STR_TO_DATE('{timestamp}', '%Y-%m-%d %H:%i:%s'),
            {lat}, {lon}, {alt}, '{callsign}'""".format(**data)
        ]
    )

def insertRocketAvionics(db, line):
    print('insertRocketAvionics not implemented yet.')


def insertPayloadAvionics(db, line):
    print('insertPayloadAvionics not implemented yet.')


def insertOther(db, line):
    print('insertOther not implemented yet.')


def importFile(filename, availFlights, db):
    '''Parses and imports a file'''
    if not os.path.isfile(filename):
        print(filename, "is not a valid filename.")
        return 0
    else:
        print("Parsing {}.".format(filename))

    validFlightIDs = displayImportMenu(availFlights)
    f_id = None
    while f_id not in validFlightIDs:
        f_id = input('Enter a Flight ID for {}: '.format(filename))

    with open(filename, 'r') as f:
        # Check the file header to see what the source is:
        insertType = {
            'BeelineGPS'        :   insertBeelineGPS,
            'Rocket_Avionics'   :   insertRocketAvionics,
            'Payload_Avionics'  :   insertPayloadAvionics,
        }.get(next(f).split()[1], insertOther)
        # Skip the csv header
        next(f)

        for line in f:
            try:
                # ugly way to process csv files and dw audio using same fn
                data = {}
                data['time'],data['lat'],data['lon'],data['alt'],data['callsign'] = line.split(',')
                insertType(db, f_id, data)
            except Exception as e:
                print(e)
                sys.exit(0)
        print("Finished importing {}.".format(filename))
        return 1;


def getParserSerial():
    ''' Read the serial number for the current pi '''
    try:
        with open('/proc/cpuinfo','r') as f:
            return f.readlines()[-1].split()[-1]
    except:
            return '0000'


def addNewFlight(db):
    ''' Attempt to create a new flight without duplicates '''
    new_fid = db.getMaxFlightID()+1
    return db.createNewActiveFlight(new_fid)


if __name__ == "__main__":
    print("ESRA 30k Rocket Parser.")

    # Connect to the ESRA database
    print("Connecting to database...", end='', flush=True)
    db = None
    try:
        db = Mariadb()
    except Exception as e:
        print(" FAILED")
        print("Start the ESRA database before running this program.")
        print("Debugging info: ",e)
        sys.exit(0)
    print(" OK")

    # Check if reading from a csv file or using audio input
    if len(sys.argv) > 1:
        # Parse input file, then quit.
        availFlights = db.getFlightTable()
        for eachFile in sys.argv[1:]:
            importFile(eachFile, availFlights, db)
        sys.exit(1)

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

    # Check status and display parser info
    f_id = db.checkActiveFlight()
    print("f_id = ", f_id)
    while not f_id:
        # f_id == None means no active flights, let's try to fix that:
        addNewFlight(db)
        f_id = db.checkActiveFlight()
    print("f_id = ", f_id)
    parser_serial = getParserSerial()
    db.registerParser(parser_serial)
    callsign = 'UNKNOWN'
    print("Parser Serial #: {}.".format(parser_serial))
    print("The current flight ID is: {}.".format(f_id))

    # Do work
    while True:
        if (datetime.datetime.now() - db.last_connected).total_seconds() > 3:
            db.updateParserTable(f_id, parser_serial, callsign)
        # Needs to be improved so this doesn't hang..
        insertBeelineGPS(db, f_id, wolf.checkAudio())

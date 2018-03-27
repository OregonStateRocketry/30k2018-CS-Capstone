from Mariadb import Mariadb

def connectDB(cf):
    # Connect to the ESRA database
    print("Connecting to database...", end='', flush=True)
    db = Mariadb(configFile=cf)
    print(" OK")
    return db

def showMenu(db):
    flights = db.getFlightTable()
    options = {}
    print("\nid || Status")
    for f in flights:
        if f['status'] == 'Active':
            options[str(f['id'])] = archiveFlight
        elif f['status'] == 'Inactive':
            options[str(f['id'])] = restoreFlight
        print("{:2d} -> {}".format( f['id'], f['status']) )

    print("Enter a flight number to toggle it: ")
    choice = input()
    if choice in options:
        options[choice](db, choice)
    else:
        print("Invalid option.")


def archiveFlight(db, id):
    sql = "UPDATE Flights SET status='Inactive' WHERE id={}".format(id)
    db.fetchSql(sql)


def restoreFlight(db, id):
    sql = "UPDATE Flights SET status='Active' WHERE id={}".format(id)
    db.fetchSql(sql)


def main(configFile):
    print("ESRA 30k Database Maintenance")
    db = connectDB(configFile)
    while True:
        showMenu(db)


if __name__ == "__main__":
    main('config.yml')

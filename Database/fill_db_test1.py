import datetime
from Mariadb import Mariadb
from time import sleep

db =  Mariadb()

def insertOne(f_id, t, lat, lon, alt, cs):
    db.insertRow(
        table = 'BeelineGPS',
        cols  = 'f_id, time, lat, lon, alt, callsign',
        vals  = ["""{f_id}, STR_TO_DATE('{timestamp}', '%Y-%m-%d %H:%i:%s'),
            {lat}, {lon}, {alt}, '{cs}'""".format(
                f_id=f_id, timestamp=t, lat=lat, lon=lon, alt=alt, cs=cs
            )
        ]
    )

if __name__ == "__main__":
    print("Running demo...")
    a = {
        'a'   : -0.05,
        'b'   : 75,
        'c'   : 5,
        'cs'  : 'Beeline1',
        'lat' : 44.5677,
        'lon' : -123.2763,
        'alt' : 5
    }
    b = {
        'a'   : -0.07,
        'b'   : 85,
        'c'   : 5,
        'cs'  : 'Beeline2',
        'lat' : 44.5677,
        'lon' : -123.2763,
        'alt' : 5
    }
    f_id = 1
    time = datetime.datetime(2018, 1, 16, 20, 20)
    for x in range(1800):
        print(x)
        for e in [a,b]:
            e['alt'] = int(e['a']*x**2+e['b']*x+e['c'])
            if e['alt'] < 0: e['alt'] = 0
            e['lat'] = round(e['lat']+float('0.00'+str(2*e['alt']**2)), 4)
            e['lon'] = round(e['lon']-float('0.00'+str(4*e['alt']**2)), 4)
            time += datetime.timedelta(seconds=1)
            # time = datetime.datetime.now()
            insertOne(f_id, time, e['lat'], e['lon'], e['alt'], e['cs'])
        sleep(1)

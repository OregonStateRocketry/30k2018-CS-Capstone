import datetime

def BeelineGPS_Parabola(fname, o_type, a, b, c, cs, time=datetime.datetime(2017, 12, 25, 6, 0)):
    print("Creating BeelineGPS_Parabola using: {}x^2+{}x+c".format(a,b,c))
    lat = 44.5677
    lon = -123.2763
    with open(fname, o_type) as f:
        # Only generate a header for new files
        if o_type == 'w':
            f.write('Source: BeelineGPS\n')
            f.write('time, lat, lon, alt, callsign\n')
        # Fill out 100 values of this formula
        for x in range(3):
            y = int(a*x**2+b*x+c)
            if y < 0: y = 0
            lat = round(lat+float('0.00'+str(2*y**2)), 4)
            lon = round(lon-float('0.00'+str(4*y**2)), 4)
            time += datetime.timedelta(seconds=1)
            f.write(
                "{time},{lat},{lon},{alt},{callsign}\n".format(
                    time=time, lat=lat, lon=lon, alt=y, callsign=cs
                )
            )

if __name__ == "__main__":
    BeelineGPS_Parabola('sample_data.txt', 'w', -0.05, 75, 5, 'Beeline1')
    BeelineGPS_Parabola('sample_data.txt', 'a', -0.07, 85, 5, 'Beeline2')
    # BeelineGPS_Parabola('sample_data.txt', 'w', -22, 1400, 5, 'Beeline1')
    # BeelineGPS_Parabola('sample_data.txt', 'a', -18, 1300, 5, 'Beeline2')

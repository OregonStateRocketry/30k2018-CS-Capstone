import fill_db_test2 as filegen
import datetime



newtime = datetime.datetime.now()
filegen.BeelineGPS_Parabola('sample_data.txt', 'w', -22, 1400, 5, 'Beeline1', newtime)
filegen.BeelineGPS_Parabola('sample_data.txt', 'a', -18, 1300, 5, 'Beeline2', newtime)

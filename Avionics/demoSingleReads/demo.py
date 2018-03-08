import MPL3115A2
import time
sensor = MPL3115A2.MPL3115A2()
i = 0
while 1:
        sensor.update()
        print(sensor.pressure())
        print(sensor.temperature())
        time.sleep(0.01)

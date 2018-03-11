import PCF8523
import time
sensor = PCF8523.PCF8523()
setter = time.localtime()
print(time.strftime('%Y-%m-%dT%H:%M:%SZ', setter))
sensor.settime(setter)
while 1:
    print(time.strftime('%Y-%m-%dT%H:%M:%SZ', sensor.gettime()))
    time.sleep(1)

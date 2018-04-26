import payloadState
import csv
import time
from random import randint
class Simulator(object):
    def __init__(self, rate, random, state):
        self.rate = rate
        self.random = random
        if state == 0:
            self.state = payloadState.PreLaunchPhase()
        if state == 1:
            self.state = payloadState.PrimaryEnginePhase()
        if state == 2:
            self.state = payloadState.SecondaryEnginePhase()
        if state == 3:
            self.state = payloadState.ExperimentPhase()
        if state == 4:
            self.state = payloadState.DescentPhase()

    def runLoop(self):

        with open("output.csv", "a+") as out:
            mycsv = csv.reader(open("input.csv"))
            for row in mycsv:
                data = {}
                data['acc_x'] = float(row[0])
                data['acc_y'] = float(row[1])
                data['acc_z'] = float(row[2])
                data['gyro_x'] = float(row[3])
                data['gyro_y'] = float(row[4])
                data['gyro_z'] = float(row[5])
                data['alt'] = int(row[6])
                self.randomer(data)
                self.state = self.state.monitorPhase(data)
                data['state'] = self.state.stateNum
                out.write("{acc_x:.3f},{acc_y:.3f},{acc_z:.3f},"
                          "{gyro_x:.3f},{gyro_y:.3f},{gyro_z:.3f},"
                          "{alt},{state}\n".format(**data))
                time.sleep(self.rate)

    def randomer(self, data):
        if(randint(0,99) < self.random):
            data['acc_x'] = float(randint(-10,10))/5
        if(randint(0,99) < self.random):
            data['acc_y'] = float(randint(-10,10))/5
        if(randint(0,99) < self.random):
            data['acc_z'] = float(randint(-10,10))/5
        if(randint(0,99) < self.random):
            data['gyro_x'] = float(randint(-10,10))/5
        if(randint(0,99) < self.random):
            data['gyro_y'] = float(randint(-10,10))/5
        if(randint(0,99) < self.random):
            data['gyro_z'] = float(randint(-10,10))/5
        if(randint(0,99) < self.random):
            data['alt'] = randint(0,40000)

if __name__ == "__main__":
    simulator = Simulator(0.01,50,1)
    simulator.runLoop()

import time
from subprocess import call
from math import sqrt

def getAvgAcc(sensors):
    return (sensors['acc_x']+sensors['acc_y']+sensors['acc_z']) / 3

def get_acc_mag(sensors):
    return sqrt(
        sensors['acc_x']**2+sensors['acc_y']**2+sensors['acc_z']**2
    )


class State(object):
    def __init__(self):
        self.stateNum = None

    def monitorPhase(self, sensors):
        ''' Implemented by the specific phases '''
        pass

    def __repr__(self):
        """Represent this object as a string"""
        # print("__repr__ = ", self.stateNum)
        return self.__str__()

    def __str__(self):
        """Describe this object by it's class name"""
        return self.__class__.__name__


class PreLaunchPhase(State):
    """
    The state before launch.
    Current conditions:
        The rocket is motionless on the launch pad.
    Duration:
        Between ~30-120 minutes.
    Goals:
        Conserve energy while waiting for launch event.
    """

    def __init__(self):
        self.stateNum           = 0
        self.duration_start     = None
        self.duration_threshold = 0.2
        self.acc_threshold      = 1.5

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            Over 1.5 G acceleration on Z axis for over 0.2 seconds.
        """
        if abs(sensors['acc_z']) > self.acc_threshold:
            if not self.duration_start:
                # First tick of acceleration sets the duration timer
                self.duration_start = time.time()
            elif (time.time() - self.duration_start) > self.duration_threshold:
                # Conditions were met, so advance phase
                return PrimaryEnginePhase()
            # Enough G's but not enough time has passed, keep checking
            return self
        else:
            # Not enough G's should reset the duration timer
            self.duration_start = None
            return self


class PrimaryEnginePhase(State):
    """
    The state during main engine burn.
    Current conditions:
        The rocket is accelerating quickly.
    Duration:
        ~10 seconds.
    Goals:
        Log sensor data.
    """

    def __init__(self):
        self.stateNum           = 1
        self.duration_start     = None
        self.duration_threshold = 0.2
        self.acc_threshold      = 1.5

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            Under 1.5 G acceleration on Z axis for over 0.2 seconds.
        """
        if abs(sensors['acc_z']) < self.acc_threshold:
            if not self.duration_start:
                # First tick of acceleration sets the duration timer
                self.duration_start = time.time()
            elif (time.time() - self.duration_start) > self.duration_threshold:
                # Conditions were met, so advance phase
                return SecondaryEnginePhase()
            # Enough G's but not enough time has passed, keep checking
            return self
        else:
            # Not enough G's should reset the duration timer
            self.duration_start = None
            return self


class SecondaryEnginePhase(State):
    """
    The state between main engine burn and apogee.
    Current conditions:
        The rocket is coasting upwards.
    Duration:
        ~20 seconds.
    Goals:
        Log sensor data.
    """

    def __init__(self):
        self.stateNum           = 2
        self.duration_threshold = 0.2
        self.long_duration_threshold = 2.0
        self.max_alt            = 0
        self.apogee_time        = False
        self.alt_threshold      = 300
        self.last_alt           = 0
        self.acc_threshold  = 0.15
        self.low_acc_flag   = False
        self.high_acc_start = False

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            Acceleration is low and
            Altitude has been descreasing for .2 seconds
        Or
            Altitude has decreased by 300 feet below local max
        """
        # Keep track of when, and how high apogee occurred

        if (sensors['alt'] > self.max_alt) & (self.low_acc_flag):
                self.max_alt = sensors['alt']
                print("set this at" + str(sensors['alt']))
        if abs(sensors['acc_z']) > self.acc_threshold:
            self.apogee_time = time.time()

        if self.apogee_time:
            if self.apogee_time+self.duration_threshold < time.time():
                self.low_acc_flag = True

        if abs(sensors['acc_z']) < self.acc_threshold:
            self.high_acc_start = time.time()
        if self.high_acc_start:
            if self.high_acc_start+self.long_duration_threshold < time.time():
                self.low_acc_flag = False
        foundapogee = False
        missedapogee = False
        if sensors['alt'] < self.max_alt:
            if self.low_acc_flag:
                foundapogee = True
        if sensors['alt'] < self.max_alt - 1000:
            missedapogee = True
        if (foundapogee or missedapogee):
            return DescentPhase()
        return self

        # # Check if the payload is nearing apogee (low acc flag set)
        # if self.low_acc_flag:
        #     if self.altitude_prev > sensors['alt']:
        #         return ExperimentPhase()
        # else:
        #     self.altitude_prev = sensors['alt']
        #     mag_acc = get_acc_mag(sensors)
        #     # Low acceleration means to start checking altitude
        #     if mag_acc < self.acc_threshold:
        #         self.low_acc_flag = True
        # return self




class DescentPhase(State):
    """
    The state during main parachute descent, after the experiment.
    Current conditions:
        The rocket is descending under main parachute.
    Duration:
        ~2 minutes.
        No more than 20 minutes.
    Goals:
        Log sensor data.
    """

    def __init__(self):
        self.stateNum           = 3
        self.duration_start     = time.time()
        self.duration_threshold = 5
        self.acc_min_threshold  = 0.9
        self.acc_max_threshold  = 1.1

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            0.9 <= |acc| < 1.1 G acceleration for over 5 seconds.
        """
        mag_acc = get_acc_mag(sensors)

        if self.acc_min_threshold < mag_acc < self.acc_max_threshold:
            if not self.duration_start:
                # First tick of acceleration sets the duration timer
                self.duration_start = time.time()
            elif (time.time() - self.duration_start) > self.duration_threshold:
                # Conditions were met, so advance phase
                return FinalPhase()
            # Enough G's but not enough time has passed, keep checking
            return self
        else:
            # Not enough G's should reset the duration timer
            self.duration_start = None
            return self

class FinalPhase(State):
    """
    The flight has concluded, close files and turn off the flight computer.
    Current conditions:
        The rocket is laying almost stationary on the ground.
    Duration:
        n/a
    Goals:
        Close the CSV file.
        Shut down.
    """

    def __init__(self):
        self.stateNum = 4

    def monitorPhase(self, sensors):
        print("Closing file handler.")
        print("Shutting down.")
        #call("sudo shutdown now", shell=True)
        raise NotImplementedError('Reached shut down')

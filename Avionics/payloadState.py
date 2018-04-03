import time
from subprocess import call

def getAvgAcc(sensors):
    return (sensors['acc_x']+sensors['acc_y']+sensors['acc_z']) / 3


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
        if sensors['acc_z'] > self.acc_threshold:
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
        if sensors['acc_z'] < self.acc_threshold:
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
        self.stateNum       = 2
        self.acc_threshold  = 0.15
        self.low_acc_flag   = False

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            Under 0.15 G magnitude of acceleration (all axis),
            THEN
            Altitude is decreasing.
        """
        if self.low_acc_flag:
            if self.altitude_prev > sensors['alt']:
                return ExperimentPhase()
        else:
            self.altitude_prev = sensors['alt']
            avg_acc = getAvgAcc(sensors)
            # Low acceleration means to start checking altitude
            if avg_acc < self.acc_threshold:
                self.low_acc_flag = True
        return self


class ExperimentPhase(State):
    """
    The state during freefall, while the experiment runs.
    Current conditions:
        The rocket is attempting to reach and maintain 0 G on Z axis
    Duration:
        ~12 seconds.
    Goals:
        Log sensor data.
        Control propeller motor.
        Control counterweight motor.
    """

    def __init__(self):
        self.stateNum           = 3
        self.duration_start     = time.time()
        self.duration_threshold = 15
        self.acc_threshold      = 1.5

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            15 seconds has elapsed.
            OR
            Over 1.5 G on Z axis (drogue deployed) (check force direction and duration on this)
        """
        if (time.time() - self.duration_start) > self.duration_threshold:
            # Experiment ends by default
            return DescentPhase()
        elif sensors['acc_z'] > self.acc_threshold: # <- check this
            # Should we check duration here too?
            return DescentPhase()
        return self

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
        self.stateNum           = 4
        self.duration_start     = time.time()
        self.duration_threshold = 5
        self.acc_min_threshold  = 0.9
        self.acc_max_threshold  = 1.1

    def monitorPhase(self, sensors):
        """
        Move to the next phase if:
            0.9 <= |acc| < 1.1 G acceleration for over 5 seconds.
        """
        avg_acc = getAvgAcc(sensors)

        if self.acc_min_threshold < avg_acc < self.acc_max_threshold:
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
        self.stateNum = 5

    def monitorPhase(self, sensors):
        print("Closing file handler.")
        print("Shutting down.")
        #call("sudo shutdown now", shell=True)
        raise NotImplementedError('Reached shut down')

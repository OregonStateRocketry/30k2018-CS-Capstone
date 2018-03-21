import time

class apogee_detect:
    """ This class takes the total acceleration and altitude as inputs
        to its primary method and outputs a 0 or 1 to indicate apogee status:
        0: apogee has not been reached
        1: apogee has been reached
    """
    # Constants that are used as threshold values
    LONG_TIMER = 4    # timer values for checking apogee
    SHORT_TIMER = 3
    VERY_CLOSE_ACCEL = 0.15   # threshold for accleration VERY close to apogee
    CLOSE_ACCEL = 0.3   # threshold for acceleration somewhat close to apogee
    MISSED_APOGEE_ACCEL = 1     #threshold for missed apogee

    #Flags and variables:
    low_acceleration = 0    # flag for accleration close to zero
    altitude_prev = 0   # Hold last checked altitude

    # timer values
    countdown_start = 0
    safety_countdown_start = 0


    # method used to compare timer values and return 1 if expired
    def check_timer(self):
        countdown_check = time.time()
        # Check timer for very close accel
        if (countdown_start)
            if(countdown_check - countdown_start >= SHORT_TIMER)
                return 1
        # Check timer for somewhat close accel
        if (safety_countdown_start)
            if (countdown_check - safety_countdown_start >= LONG_TIMER)
                return 1
        return 0

    def check_apogee(self, acceleration, altitude):
        # if acceleration is close to apogee and starts decreasing, respond apogee
        if (low_acceleration)
            # Zero is used here for comparison, but some implementations use a
            # threshold value to make sure altitude is really decreasing
            if (altitude_prev - altitude) > 0
                return 1    # respond with apogee

        # check apogee countdown
        check_countdown_timers = check_timer()
        if (check_countdown_timers)
            return 1

        # check acceleration against threshold
        if (acceleration < VERY_CLOSE_ACCEL)
            # set flag to check altitude
            low_acceleration = 1

            # start countdown
            if (countdown_start == 0) countdown_start = time.time()
            altitude_prev = altitude
            return 0

        # check acceleration against higher threshold
        if (acceleration < CLOSE_ACCEL)
            # start safety countdown
            if (safety_countdown_start == 0) safety_countdown_start = time.time()
            altitude_prev = altitude
            return 0

        # check for free fall -- was apogee missed completely?
        if(acceleration > MISSED_APOGEE_ACCEL)
            return 1 # apogee was missed

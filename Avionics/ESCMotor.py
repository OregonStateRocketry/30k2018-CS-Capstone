import pigpio, time, sys

class Motor:
    '''Tools to control and interface with the ESC and brushless motor'''
    #######	Example	PID values #########
    #p=PID(3.0,0.4,1.2)
    #p.setPoint(5.0)
    #while True:
    #     pid = p.update(measurement_value)

    def __init__(self, pi, pin, DC=False, pinR=None, P=2.0, I=0.0, D=1.0, goal=0.0):
        # PID components
        self.pi             = pi
        self.Kp             = P
        self.Ki             = I
        self.Kd             = D
        self.set_point      = goal
        self.clear()

        # Motor components
        self.ESC_MIN        = 800
        self.ESC_MAX        = 1800
        self.PIN            = pin
        self.PIN_R          = pinR
        self.TYPE_DC        = DC

        # Set up either ESC or DC motor
        if self.TYPE_DC:
            # Set PWM range to match the ESC input range
            self.pi.set_PWM_range(self.PIN, self.ESC_MAX-self.ESC_MIN)
            # Will need to refactor to use the reverse pin
            # self.pi.set_PWM_range(self.PIN_R, self.ESC_MAX-self.ESC_MIN)

        # Enable motor output pins
        self.pi.set_mode(self.PIN, pigpio.OUTPUT)
        self.set_motor(self.ESC_MIN)


    def __del__(self):
        ''' Ensure the motor stops when this object is destroyed '''
        self.stop()


    def clear(self):
        self.PTerm          = 0.0
        self.ITerm          = 0.0
        self.DTerm          = 0.0
        self.last_error     = 0.0
        self.windup_guard   = 20
        self.last_time      = time.time()


    def stop(self):
        ''' Stop the motor '''
        self.set_motor(self.ESC_MIN)


    def pid_to_pwm(self, pid):
        '''Converts from one range of numbers to another'''
        pwm_min, pwm_max = self.ESC_MIN, self.ESC_MAX
        pid_min, pid_max = -self.Kp*2, self.Kp*2     # Are PID values always positive?

        if pid<pid_min: pid = pid_min
        if pid>pid_max: pid = pid_max

        pid_range = (pid_max - pid_min)
        pwm_range = (pwm_max - pwm_min)
        return int((((pid - pid_min) * pwm_range) / pid_range) + pwm_min)


    def set_motor(self, speed):
        '''Set the motor speed to a PWM value'''
        if self.ESC_MIN <= speed <= self.ESC_MAX:
            # Two types of motors use this library:
            if self.TYPE_DC:    # DC motors
                # Remember: the PWM range is 0 to (MAX - MIN)
                # speed will be between MIN and MAX, so subtract MIN here
                self.pi.set_PWM_dutycycle(self.PIN, speed-self.ESC_MIN)
            else:               # Brushless motors w/ESC
                self.pi.set_servo_pulsewidth(self.PIN, speed)
            return True
        return False


    def update_motor(self, current_value):
        '''Takes acceleration, updates PID and motor'''
        PID = self.update(current_value)
        PWM = self.pid_to_pwm(-PID)
        self.set_motor(PWM)
        return (PID, PWM)


    def update(self, current_value):
        """
        Calculate PID output value for given reference input and feedback
        u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}
        """
        # How wrong is our measurement?
        error = self.set_point - current_value
        delta_error = error - self.last_error

        # How long has it been since our last adjustment?
        current_time = time.time()
        delta_time = current_time - self.last_time

        self.PTerm = self.Kp * error

        # Prevent runaway I gain which causes overshoot
        self.ITerm += error * delta_time
        if self.ITerm < -self.windup_guard:
            self.ITerm = -self.windup_guard
        elif self.ITerm > self.windup_guard:
            self.ITerm = self.windup_guard

        self.DTerm = delta_error / delta_time

        # Save results for next loop
        self.last_time = current_time
        self.last_error = error

        return self.PTerm + self.Ki * self.ITerm + self.Kd * self.DTerm

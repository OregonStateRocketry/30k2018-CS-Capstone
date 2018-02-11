import pigpio, time, sys

class Motor:
    '''Tools to control and interface with the ESC and brushless motor'''
    #######	Example	PID values #########
    #p=PID(3.0,0.4,1.2)
    #p.setPoint(5.0)
    #while True:
    #     pid = p.update(measurement_value)

    def __init__(self, pi, pin, P=2.0, I=0.0, D=1.0, Z=0.0):
        # PID components
        self.pi             = pi
        self.Kp             = P
        self.Ki             = I
        self.Kd             = D
        self.set_point      = Z
        self.clear()

        # Motor components
        self.ESC_MIN        = 1000
        self.ESC_MAX        = 2000
        self.PIN            = pin

        # Enable ESC output pin
        self.pi.set_mode(self.PIN, pigpio.OUTPUT)

    def clear(self):
        self.PTerm          = 0.0
        self.ITerm          = 0.0
        self.DTerm          = 0.0
        self.last_error     = 0.0
        self.windup_guard   = 20
        self.last_time      = time.time()

    def set_ESC_range(self, low=1000, high=2000):
        '''Configure input range on ESC, MUST run while ESC is starting!'''
        'Times are arbitrary, but these take a few seconds.'
        self.pi.set_servo_pulsewidth(self.PIN, low)
        time.sleep(10)
        self.pi.set_servo_pulsewidth(self.PIN, high)
        time.sleep(3)
        self.pi.set_servo_pulsewidth(self.PIN, 0)     # off
        time.sleep(2)
        return True

    def pid_to_pwm(self, pid):
        '''Converts from one range of numbers to another'''
        pwm_min, pwm_max = self.ESC_MIN, self.ESC_MAX
        pid_min, pid_max = 0.0, self.Kp*2     # Are PID values always positive?

        if pid<pid_min: pid = pid_min
        if pid>pid_max: pid = pid_max

        pid_range = (pid_max - pid_min)
        pwm_range = (pwm_max - pwm_min)
        return int((((pid - pid_min) * pwm_range) / pid_range) + pwm_min)

    def set_motor(self, speed):
        '''Set the motor speed to a PWM value'''
        if self.ESC_MIN <= speed <= self.ESC_MAX:
            self.pi.set_servo_pulsewidth(self.PIN, speed)
            return True
        print("Bad value")
        return False

    def update_motor(self, current_value):
        '''Takes acceleration, updates PID and motor'''
        PID = self.update(current_value)
        PWM = self.pid_to_pwm(PID)
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

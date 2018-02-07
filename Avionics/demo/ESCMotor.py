import pigpio, time, sys

class Motor:
    '''Tools to control and interface with the ESC and brushless motor'''
    #######	Example	PID values #########
    #p=PID(3.0,0.4,1.2)
    #p.setPoint(5.0)
    #while True:
    #     pid = p.update(measurement_value)

    def __init__(self, pi, pin, P=2.0, I=0.0, D=1.0, Z=0.0):
        self.pi = pi
        self.Kp             = P
        self.Ki             = I
        self.Kd             = D
        self.set_point      = Z
        self.Derivator      = 0
        self.Integrator     = 0
        self.Integrator_max = 500
        self.Integrator_min = -500
        self.error          = 0.0

        self.ESC_MIN        = 1000
        self.ESC_MAX        = 2000
        self.PIN            = pin

        # Enable ESC output pin
        self.pi.set_mode(self.PIN, pigpio.OUTPUT)

    def set_ESC_range(self, low=1000, high=2000):
        '''Configure input range on ESC, MUST run while ESC is starting!'''
        'Times are arbitrary, but these take a few seconds.'
        pi.set_servo_pulsewidth(PIN, low)
        time.sleep(10)
        pi.set_servo_pulsewidth(PIN, high)
        time.sleep(3)
        pi.set_servo_pulsewidth(PIN, 0)     # off
        time.sleep(2)
        return True

    def pid_to_pwm(self, pid):
        '''Converts from one range of numbers to another'''
        pwm_min, pwm_max = self.ESC_MIN, self.ESC_MAX
        pid_min, pid_max = 0.0, self.Kp     # Are PID values always positive?

        if pid<pid_min: pid = pid_min
        if pid>pid_max: pid = pid_max

        pid_range = (pid_max - pid_min)
        pwm_range = (pwm_max - pwm_min)
        return (((pid - pid_min) * pwm_range) / pid_range) + pwm_min

    def set_motor(self, speed):
        '''Set the motor speed to a PWM value'''
        if self.MIN < speed < self.MIN:
            pi.set_servo_pulsewidth(PIN, speed)
            return True
        return False

    def update_motor(self, current_value):
        '''Takes acceleration, updates PID and motor'''
        PID = update(current_value)
        PWM = pid_to_pwm(PID)
        set_motor(PWM)
        return PWM


    def update(self,current_value):
        """
        Calculate PID output value for given reference input and feedback
        """
        self.error = self.set_point - current_value

        self.P_value = self.Kp * self.error
        self.D_value = self.Kd * ( self.error - self.Derivator)
        self.Derivator = self.error

        self.Integrator = self.Integrator + self.error

        if self.Integrator > self.Integrator_max:
            self.Integrator = self.Integrator_max
        elif self.Integrator < self.Integrator_min:
            self.Integrator = self.Integrator_min

        self.I_value = self.Integrator * self.Ki

        PID = self.P_value + self.I_value + self.D_value

        return PID

    def setPoint(self,set_point):
        """
        Initilize the setpoint of PID
        """
        self.set_point  = set_point
        self.Integrator = 0
        self.Derivator  = 0

    def setIntegrator(self, Integrator):
        self.Integrator = Integrator

    def setDerivator(self, Derivator):
        self.Derivator = Derivator

    def setKp(self,P):
        self.Kp = P

    def setKi(self,I):
        self.Ki = I

    def setKd(self,D):
        self.Kd = D

    def getPoint(self):
        return self.set_point

    def getError(self):
        return self.error

    def getIntegrator(self):
        return self.Integrator

    def getDerivator(self):
        return self.Derivator

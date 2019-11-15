import math

class Robot():
    def __init__(self):
        self._right_motor = 0.0
        self._left_motor = 0.0
        self._right_motor_vel = 0.0
        self._left_motor_vel = 0.0
        self._right_motor_k = 1.0
        self._left_motor_k = 1.0
        self._x = 0.0
        self._y = 0.0
        self._heading = 0.0
        self.max_vel = 1
        self.min_vel = -1

    def loop(self, dt):
        return

    def set_right_motor(self, value):
        self._right_motor_vel = max(min(value, self.max_vel), self.min_vel)

        
    
    def set_left_motor(self, value):
        self._left_motor_vel = max(min(value, self.max_vel), self.min_vel)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_heading(self):
        return self._heading

    def print_graphs(self):
        return

    def _integrate_motors(self, dt):
        # self._right_motor_vel += dt * (self._right_motor - self._right_motor_vel)
        # self._left_motor_vel += dt * (self._left_motor - self._left_motor_vel)
        
        self._dforward = (self._left_motor_k * self._left_motor_vel + self._right_motor_k * self._right_motor_vel) * (1. / 2.)
        self._dheading = (self._right_motor_k * self._right_motor_vel - self._left_motor_k * self._left_motor_vel) * (1. / 2.)


        self._x += dt * self._dforward * math.cos(self._heading)
        self._y += dt * self._dforward * math.sin(self._heading)
        self._heading += dt * self._dheading + 2. * math.pi
        self._heading = math.fmod(self._heading, 2. * math.pi)
        return


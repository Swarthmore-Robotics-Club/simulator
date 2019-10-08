import math

class Robot(object):
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

    def loop(self, dt):
        pass

    def set_right_motor(self, value):
        self._right_motor = max(min(value, 1.0), -1.0)
    
    def set_left_motor(self, value):
        self._left_motor = max(min(value, 1.0), -1.0)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_heading(self):
        return self._heading

    def _integrate_motors(self, dt):
        self._right_motor_vel += dt * (self._right_motor - self._right_motor_vel)
        self._left_motor_vel += dt * (self._left_motor - self._left_motor_vel)
        
        forward_vel = (self._left_motor_k * self._left_motor_vel + self._right_motor_k * self._right_motor_vel) * (1. / 2.)
        heading_vel = (self._left_motor_k * self._left_motor_vel - self._right_motor_k * self._right_motor_vel) * (1. / 2.)

        self._x += dt * forward_vel * math.cos(self._heading)
        self._y += dt * forward_vel * math.sin(self._heading)
        self._heading += dt * heading_vel + 2. * math.pi
        self._heading = math.fmod(self._heading, 2. * math.pi)

class World(object):
    def __init__(self, robot):
        self.robot = robot

    def loop(self, dt):
        self.robot.loop(dt)
        self.robot._integrate_motors(dt)

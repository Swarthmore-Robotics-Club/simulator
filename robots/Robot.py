import math

TICKS_PER_REVOLUTION = 2750
BASE_WHEEL_RADIUS = 0.02
TWO_PI = 2 * math.pi

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
        self.wheel_radius = BASE_WHEEL_RADIUS
        self.encoder_ticks_per_wheel_rev = TICKS_PER_REVOLUTION
        self._ticks_left = 0
        self._ticks_right = 0
        return

    def loop(self, dt):
        return

    def set_right_motor(self, value):
        self._right_motor_vel = max(min(value, self.max_vel), self.min_vel)
        return

    def set_left_motor(self, value):
        self._left_motor_vel = max(min(value, self.max_vel), self.min_vel)
        return

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_heading(self):
        return self._heading

    def read_encoders(self):
        return (int(self._ticks_left), int(self._ticks_right))

    def print_graphs(self):
        return

    def _integrate_motors(self, dt):
        left_distance = (self._left_motor_vel) * dt
        left_wheel_revs = left_distance / (self.wheel_radius * TWO_PI)
        self._ticks_left += left_wheel_revs * self.encoder_ticks_per_wheel_rev
        right_distance = (self._right_motor_vel) * dt
        right_wheel_revs = right_distance / (self.wheel_radius * TWO_PI)
        self._ticks_right += right_wheel_revs * self.encoder_ticks_per_wheel_rev

        self._dforward = (self._left_motor_k * self._left_motor_vel + self._right_motor_k * self._right_motor_vel) / 2
        self._dheading = (self._right_motor_k * self._right_motor_vel - self._left_motor_k * self._left_motor_vel) / 2
        self._x += dt * self._dforward * math.cos(self._heading)
        self._y += dt * self._dforward * math.sin(self._heading)
        self._heading += dt * self._dheading + TWO_PI
        self._heading = math.fmod(self._heading, TWO_PI)
        return

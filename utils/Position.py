import math

TWO_PI = math.pi * 2

class Position():
    def __init__(self, starting_x, starting_y, starting_heading, wheel_radius, ticks_per_rev):
        self.x = starting_x
        self.y = starting_y
        self.heading = starting_heading
        self.wheel_radius = wheel_radius
        self.encoder_ticks_per_wheel_rev = ticks_per_rev
        self._previous_ticks = (0, 0)
        return
    

    def update(self, ticks, sensor_readings):
        ticks_left, ticks_right = ticks
        diff_ticks_left = ticks_left - self._previous_ticks[0]
        diff_ticks_right = ticks_right - self._previous_ticks[1]
        self._previous_ticks = (ticks_left, ticks_right)

        d_left_wheel = TWO_PI * self.wheel_radius * (diff_ticks_left / self.encoder_ticks_per_wheel_rev)
        d_right_wheel = TWO_PI * self.wheel_radius * (diff_ticks_right / self.encoder_ticks_per_wheel_rev)
        d_center = (d_left_wheel + d_right_wheel) / 2

        self.x = self.x + (d_center * math.cos(self.heading))
        self.y = self.y + (d_center * math.sin(self.heading))
        self.heading = math.fmod(self.heading + ((d_right_wheel - d_left_wheel) / 2) + TWO_PI, TWO_PI)

        self._parse_sensor_data(sensor_readings)
        return


    def _parse_sensor_data(self, sensor_readings):
        return

    
    def as_tuple(self):
        return (self.x, self.y, self.heading)
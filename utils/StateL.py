from enum import Enum
import math
from DFSL import DFSL, tp
from PIDLoop import PIDLoop
from robots.Robot import TICKS_PER_REVOLUTION

TWO_PI = math.pi * 2

class BigBrother(Enum):
    NOT_ENOUGH_TAXES = 3
    GREAT_LEAP_FORWARD = 1984
    PRAGUE_SPRING = 3300000


class ThePartyL():
    def __init__(self, labyrinth, callback, robot, starting_loc):
        self.dfs = DFSL(labyrinth, labyrinth.get_goal(), callback)
        self.robot = robot
        self.state = BigBrother.NOT_ENOUGH_TAXES
        self.next_cell = tuple()
        self.angle_ticker = 0
        self.prev_ticks_left = 0
        self.prev_ticks_right = 0
        self.position = (*starting_loc, 0.0) # x, y, heading

        self.angle_pid = PIDLoop(5, 0, 0.1)
        self.power_val = 2
        self.acceptable_angle_error = .1
        self.acceptable_physical_offset = 0.01
        self.ticks_needed = 100

        self.wheel_radius = 0.02 # meters
        self.wheel_base_length = 0.09 # meters
        self.max_vel = 0.3 # m/s
        return


    def get_velocities(self, real_x, real_y, heading, dt):
        x, y = self.position[:2]
        if self.state == BigBrother.NOT_ENOUGH_TAXES:
            self.next_cell = self.get_next_cell(x, y, real_x, real_y, heading)
            self.state = BigBrother.PRAGUE_SPRING
        self._update_position()
        angle_error = self.get_angle_error(x, y, heading)
        angular_vel = self.angle_pid.updateErrorPlus(angle_error, dt)
        if self.state == BigBrother.PRAGUE_SPRING:
            if abs(angle_error) < self.acceptable_angle_error:
                if self.angle_ticker < self.ticks_needed:
                    self.angle_ticker += 1
                else:
                    self.angle_ticker = 0
                    self.state = BigBrother.GREAT_LEAP_FORWARD
            else:
                self.angle_ticker = 0
            return self.get_individual_proportions(0, angular_vel)
        if self.state == BigBrother.GREAT_LEAP_FORWARD:
            if self.should_slow_down(x, y):
                return self.slow_down_comrade()
            vel = self.max_vel / (abs(angular_vel) + 1)**self.power_val # drops to 0
            return self.get_individual_proportions(vel, angular_vel)
        raise Exception('ruh roh raggy')


    def _update_position(self):
        ticks_left, ticks_right = self.robot.read_encoders()
        #print('left ticks: {}, right ticks: {}'.format(ticks_left, ticks_right))
        diff_ticks_left = ticks_left - self.prev_ticks_left
        diff_ticks_right = ticks_right - self.prev_ticks_right
        self.prev_ticks_left = ticks_left
        self.prev_ticks_right = ticks_right

        d_left_wheel = TWO_PI * self.wheel_radius * (diff_ticks_left / TICKS_PER_REVOLUTION)
        d_right_wheel = TWO_PI * self.wheel_radius * (diff_ticks_right / TICKS_PER_REVOLUTION)
        d_center = (d_left_wheel + d_right_wheel) / 2

        prev_x, prev_y, prev_heading = self.position
        new_x = prev_x + (d_center * math.cos(prev_heading))
        new_y = prev_y + (d_center * math.sin(prev_heading))
        new_heading = math.fmod(prev_heading + ((d_right_wheel - d_left_wheel) / 2) + TWO_PI, TWO_PI)
        self.position = (new_x, new_y, new_heading)
        # print('In with the new pos: {}'.format(tuple(map(lambda x: round(x, 4), self.position))))
        return


    def get_angle_error(self, x, y, heading):
        desired_angle = math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)
        diff = desired_angle - heading
        return math.atan2(math.sin(diff), math.cos(diff))


    def should_slow_down(self, x, y):
        return abs(self.next_cell[0] - x) < self.acceptable_physical_offset and abs(self.next_cell[1] - y) < self.acceptable_physical_offset


    def slow_down_comrade(self):
        self.state = BigBrother.NOT_ENOUGH_TAXES
        return (0, 0)


    def get_next_cell(self, x, y, real_x, real_y, heading):
        cell = self.dfs.get_next_cell(x, y, (real_x, real_y), heading)
        print('Reality: {}, belief: {}\n\tNext cell: {}'.format(tp((real_x, real_y, heading)), tp(self.position), cell))
        return cell


    def get_individual_proportions(self, vel, a_vel):
        l_vel, r_vel = self.unicycle_to_differential_drive(vel, a_vel)
        m = max(abs(l_vel), abs(r_vel))
        if m == 0:
            m = 1
        return l_vel / m, r_vel / m

    """
    velocity -> forward velocity, m/s
    angular_velocity > angular velocity, radians/s

    @returns left and right wheel velocities (in m/s?)
    see http://faculty.salina.k-state.edu/tim/robotics_sg/Control/kinematics/unicycle.html
    """
    def unicycle_to_differential_drive(self, velocity, angular_velocity):
        radius = self.wheel_radius
        length = self.wheel_base_length
        left_vel = (2 * velocity - angular_velocity * length) / (2 * radius)
        right_vel = (2 * velocity + angular_velocity * length) / (2 * radius)
        return left_vel, right_vel

from enum import Enum
from PIDLoop import PIDLoop
from DFS import DFS
import math

TWO_PI = math.pi * 2
class BigBrother(Enum):
    NOT_ENOUGH_TAXES = 3
    GREAT_LEAP_FORWARD = 1984
    PRAGUE_SPRING = 3300000


class TheParty():
    def __init__(self, maze, callback):
        self.state = BigBrother.NOT_ENOUGH_TAXES
        self.next_cell = None # tuple

        # next 5 lines have hardcoded vals that should be played with
        self.angle_pid = PIDLoop(5, 0, 0.1)
        self.power_val = 2
        self.acceptable_angle_error = .1
        self.acceptable_physical_offset = 0.01
        self.ticks_needed = 100

        # next 3 lines should be set w/ our real params
        self.wheel_radius = 0.02 # meters
        self.wheel_base_length = 0.08 # meters
        self.max_vel = 0.3 # m/s

        self.angle_ticker = 0
        self.vel_ticker = 0
        self.dfs = DFS(maze, maze.get_goal(), callback)
        return


    def get_velocities(self, x, y, heading, dt):
        if self.state == BigBrother.NOT_ENOUGH_TAXES:
            self.next_cell = self.get_next_cell(x, y)
            self.state = BigBrother.PRAGUE_SPRING
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


    def get_angle_error(self, x, y, heading):
        desired_angle = math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)
        diff = desired_angle - heading
        if abs(diff) <= math.pi:
            return diff
        if diff > math.pi:
            return diff - TWO_PI
        return diff + TWO_PI


    def should_slow_down(self, x, y):
        return abs(self.next_cell[0] -x) < self.acceptable_physical_offset and abs(self.next_cell[1] - y) < self.acceptable_physical_offset


    def slow_down_comrade(self):
        self.state = BigBrother.NOT_ENOUGH_TAXES
        return (0,0)


    def get_next_cell(self, x, y):
        cell = self.dfs.get_next_cell(x, y)
        print('hi we got a new cell mister here it is sire {}'.format(cell))
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
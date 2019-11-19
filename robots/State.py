from enum import Enum
from robots.PIDLoop import PIDLoop
from robots.DFS import DFS
import math

TWO_PI = math.pi * 2
class BigBrother(Enum):
    NOT_ENOUGH_TAXES = 3
    GREAT_LEAP_FORWARD = 1984
    PRAGUE_SPRING = 3300000



class TheParty():
    def __init__(self, maze):
        self.state = BigBrother.NOT_ENOUGH_TAXES
        self.next_cell = None # tuple

        # next 2 lines have hardcoded floats that should be played with
        self.angle_pid = PIDLoop(5, 0, 0.1)
        self.power_val = 2

        # next 3 lines should be set w/ our real params
        self.wheel_radius = 0.02 # meters
        self.wheel_base_length = 0.08 # meters
        self.max_vel = 0.3 # m/s

        self.angle_ticker = 0
        self.vel_ticker = 0
        self.dfs = DFS(maze, maze.get_goal(), self.no_op)
        return
    
    def no_op(self):
        return

    def get_velocities(self, x, y, heading, dt):
        THRESHOLD_VAL = .1
        if self.state == BigBrother.NOT_ENOUGH_TAXES:
            self.next_cell = self.get_next_cell(x, y)
            self.state = BigBrother.PRAGUE_SPRING
        desired_angle = self.get_desired_angle(x, y)
        angle_error = desired_angle - heading # should be pos if we want to go left, neg otherwise
        if angle_error > math.pi:
            angle_error -= TWO_PI
        elif angle_error < -math.pi:
            angle_error += TWO_PI
        angular_vel = self.angle_pid.updateErrorPlus(angle_error, dt) 
        if self.state == BigBrother.PRAGUE_SPRING:
            print('real diff : {:2.4}'. format(abs(desired_angle - heading)))
            if abs(desired_angle - heading) < THRESHOLD_VAL:
                if self.angle_ticker < 100:
                    self.angle_ticker += 1
                else:
                    self.angle_ticker = 0
                    self.state = BigBrother.GREAT_LEAP_FORWARD
            else:
                print('\tResetting angle ticker')
                self.angle_ticker = 0
            return self.get_individual_proportions(0, angular_vel)
        if self.state == BigBrother.GREAT_LEAP_FORWARD:
            if self.should_slow_down(x, y, THRESHOLD_VAL):
                return self.slow_down_comrade()
            vel = self.max_vel / (abs(angular_vel) + 1)**self.power_val # drops to 0
            return self.get_individual_proportions(vel, angular_vel)
        raise Exception('ruh roh raggy')


    def get_desired_angle(self, x, y):
        return math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)


    def should_slow_down(self, x, y, THRESHOLD_VAL = .1):
        return abs(self.next_cell[0] -x) < THRESHOLD_VAL and abs(self.next_cell[1] - y) < THRESHOLD_VAL


    def slow_down_comrade(self):
        self.state = BigBrother.NOT_ENOUGH_TAXES
        return (0,0)


    def get_next_cell(self, x, y):

        cell = self.dfs.get_next_cell(x, y)
        print("hi we got a new cell mister here it is sire {}".format(cell))
        return cell 


    def get_individual_proportions(self, vel, a_vel):
        l_vel, r_vel = self.unicycle_to_differential_drive(vel, a_vel)
        m = max(abs(l_vel), abs(r_vel))
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
from enum import Enum
from robots import PIDLoop
import math


class BigBrother(Enum):
    NOT_ENOUGH_TAXES = 3
    GREAT_LEAP_FORWARD = 1984
    PRAGUE_SPRING = 3300000



"""
Three things here


"""

class TheParty():
    def __init__(self):
        self.state = BigBrother.NOT_ENOUGH_TAXES
        self.next_cell = None # tuple

        # next 2 lines have hardcoded floats that should be played with
        self.angle_pid = PIDLoop(5, 0, 0.5)
        self.power_val = 2

        # next 3 lines should be set w/ our real params
        self.wheel_radius = 0.02 # meters
        self.wheel_base_length = 0.08 # meters
        self.max_vel = 0.3 # m/s

        self.angle_ticker = 0
        self.vel_ticker = 0
        
        return


    def get_velocities(self, x, y, heading):

        """
            
        """
        if self.state == BigBrother.NOT_ENOUGH_TAXES:
            self.next_cell = self.get_next_cell(x, y)
            self.state = BigBrother.PRAGUE_SPRING
        elif self.state == BigBrother.PRAGUE_SPRING:
            
            # want to get desired angle using given heading and knowing 
            desired_angle = get_desired_angle( self.next_cell.x, self.next_cell.y)

            THRESHOLD_VAL = .1
            # if the difference of our heading is within our tick range
            if abs(desired_angle - heading) < THRESHOLD_VAL:

                if self.angle_ticker < 100:
                    self.angle_ticker += 1
                else:
                    # if we are in the ticker then we set the motors
                    self.angle_ticker = 0
                    # return self.slow_down_comrade()
                    self.state = BigBrother.GREAT_LEAP_FORWARD
                
                    return (1,1)

        elif self.state == BigBrother.GREAT_LEAP_FORWARD:
            # LEAP FORWARD

            if self.should_slow_down():
                return self.slow_down_comrade()

            return (1, 1)
                    
            

        return (1, 1)

    
    def straight_forward_leap(self):
        pass

    def should_slow_down(self, x, y, THRESHOLD_VAL = .1):
        return abs(self.next_cell[0] -x ) < THRESHOLD_VAL and abs(self.next_cell[1] - y) < THRESHOLD_VAL

    def slow_down_comrade(self):
        return (0,0)

    def get_next_cell(self, x, y, maze = []):
        return (1, 0)

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

    def get_desired_angle(self, x, y):
        next_cell = self.dfs.get_next_cell(x, y)
        arctan = math.atan2(next_cell[1] - y, next_cell[0] - x)
        return arctan
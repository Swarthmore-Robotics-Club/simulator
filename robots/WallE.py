import math
import matplotlib.pyplot as plt
import random
from PIDLoop import PIDLoop
from Robot import Robot

TWO_PI = 2 * math.pi

"""
starts at 0.5, 0.5 facing East. Wants to check where it can go. Goal is top right.
"""
class WallE(Robot):
    def __init__(self, maze):
        Robot.__init__(self)
        self.maze = maze
        self.goal = self.maze.get_goal()
        self.next_cell = None
        self.already_visited = set()
        self.headings = []
        self.desired_angles = []
        self.xs = []
        self.ys = []

        # next 2 lines have hardcoded floats that should be played with
        self.angle_pid = PIDLoop(5, 0, 0)
        self.power_val = 3

        # next 3 lines should be set w/ our real params
        self.wheel_radius = 0.02 # meters
        self.wheel_base_length = 0.08 # meters
        self.max_vel = 0.3 # m/s

        # next 2 lines are hacky way to set the initial position appropriately
        # don't want to set in Robot.py because that screws up earlier bots
        self._x = 0.5
        self._y = 0.5
        return

    """
    TODO: think the problem is l_vel and r_vel are almost always well above 1 or below -1 so their changes
    aren't captured by our .setmotor() - might have been fixed by get_individual_proportions()

    TODO: can't seem to turn right directly - see current graphss
    """
    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()

        if x < -1 or y < -1 or y > self.maze._max_y + 2 or x > self.maze._max_x + 2:
            raise Exception('x: {}, y: {}'.format(x, y))
        heading = self.get_heading()
        # depending on where we are on the maze, we want to change our desired angle
        desired_angle = self.get_desired_angle(x, y)
        # get the error in our angluar velocity using PID, maybe want to 
        angular_vel = self.angle_pid.updateErrorPlus(desired_angle - heading, dt) 

        vel = self.max_vel / (abs(angular_vel) + 1)**self.power_val # drops to 0 pretty fast as angular_vel increases, turn slowly
        l_vel, r_vel = self.get_individual_proportions(vel, angular_vel)
        print('angular vel: {:2.4}, nextcell: {}, desired left wheel vel: {:2.4}, actual left wheel vel {:2.4}, desired right wheel vel: {:2.4}, actual right wheel vel {:2.4}, heading: {:2.4}'.format(angular_vel, self.next_cell, l_vel, self._left_motor_vel, r_vel, self._right_motor_vel, heading))
        self.set_left_motor(l_vel)
        self.set_right_motor(r_vel)
        self.headings.append(heading)
        self.desired_angles.append(desired_angle)
        self.xs.append(x)
        self.ys.append(y)
        return


    def get_desired_angle(self, x, y):
        """
            given the robot's position and its final goal, returns the angle that
            theoretically would get the robot closer to its goal
        """


        if self.next_cell:
            acceptable_offset = 0.1
            # acceptable_offset = .04
            desired_x = self.next_cell[0]
            desired_y = self.next_cell[1]
            if abs(desired_x - x) <= acceptable_offset and abs(desired_y - y) <= acceptable_offset:
                if desired_x == self.goal[0] and desired_y == self.goal[1]:
                    raise Exception('We done here', self.goal, x, y)
                self.next_cell = None

        if not self.next_cell:
            options = []
            """
            Floor x and y because while we're aiming for the center of each square
            i.e. x and y offset at x.5 and y.5, the maze thinks of an entire square
            as defined by it's lower left point
            """
            floor_x = math.floor(x)
            perfect_x = floor_x + .5
            floor_y = math.floor(y)
            perfect_y = floor_y + .5
            if self.maze.can_up(floor_x, floor_y):
                options.append((perfect_x, perfect_y + 1))
            if self.maze.can_right(floor_x, floor_y):
                options.append((perfect_x + 1, perfect_y))
            if self.maze.can_down(floor_x, floor_y):
                options.append((perfect_x, perfect_y - 1))
            if self.maze.can_left(floor_x, floor_y):
                options.append((perfect_x - 1, perfect_y))
            for option in options:
                if option not in self.already_visited:
                    self.already_visited.add(option)
                    self.next_cell = option
                    break
            if not self.next_cell:
                self.next_cell = random.choice(options)
            print('Next cell: ', self.next_cell)
        

        arctan = math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)

        #  if arctan is negative and not in the lower right quadrant, we want to rotate right
        # TODO SEE IF KEEPING ATAN NEGATIVE IN LOWER 4TH QUADRANT IS GOOD
        if arctan < 0 and not arctan >= (3/2) * TWO_PI and not arctan < TWO_PI:
            arctan += TWO_PI

        return arctan


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


    def print_graphs(self):
        fig = plt.figure()

        plt.subplot(1, 2, 1)
        plt.plot(range(len(self.headings)), self.headings)
        plt.plot(range(len(self.desired_angles)), self.desired_angles)

        plt.subplot(1, 2, 2)
        plt.plot(self.xs, self.ys)
        for y in range(len(self.maze.maze)):
            for x in range(len(self.maze.maze[y])):
                if not self.maze.can_down(x, y):
                    plt.plot([x, x + 1], [y, y], color='gray')
                if not self.maze.can_left(x, y):
                    plt.plot([x, x], [y, y + 1], color='gray')
                if not self.maze.can_right(x, y):
                    plt.plot([x + 1, x + 1], [y, y + 1], color='gray')
                if not self.maze.can_up(x, y):
                    plt.plot([x, x + 1], [y + 1, y + 1], color='gray')

        plt.show()
        return

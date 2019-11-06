import math
import matplotlib.pyplot as plt
from DFS import DFS
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
        self.dfs = DFS(self.maze, self.maze.get_goal(), self.set_race_start)
        self.headings = []
        self.desired_angles = []
        self.xs = []
        self.ys = []
        self.race_start = 0

        # next 2 lines have hardcoded floats that should be played with
        self.angle_pid = PIDLoop(5, 0, 0.5)
        self.power_val = 2

        # next 3 lines should be set w/ our real params
        self.wheel_radius = 0.02 # meters
        self.wheel_base_length = 0.08 # meters
        self.max_vel = 0.3 # m/s

        # next 2 lines are hacky way to set the initial position appropriately
        # don't want to set in Robot.py because that screws up earlier bots
        self._x = 0.5
        self._y = 0.5
        return


    def set_race_start(self):
        self.race_start = len(self.xs)
        return


    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        if x < -1 or y < -1 or y > self.maze._max_y + 2 or x > self.maze._max_x + 2:
            raise Exception('x: {}, y: {}'.format(x, y))
        heading = self.get_heading()
        if heading > math.pi:
            heading -= 2 * math.pi
        desired_angle = self.get_desired_angle(x, y)
        angle_error = desired_angle - heading # should be pos if we want to go left, neg otherwise
        if angle_error > math.pi:
            angle_error -= TWO_PI
        elif angle_error < -math.pi:
            angle_error += TWO_PI
        angular_vel = self.angle_pid.updateErrorPlus(angle_error, dt) 

        vel = self.max_vel / (abs(angular_vel) + 1)**self.power_val # drops to 0 pretty fast as angular_vel increases, turn slowly
        l_vel, r_vel = self.get_individual_proportions(vel, angular_vel)
        # print('angular vel: {:2.4}, desired left wheel vel: {:2.4}, actual left wheel vel {:2.4}, desired right wheel vel: {:2.4}, actual right wheel vel {:2.4}, heading: {:2.4}'.format(angular_vel, l_vel, self._left_motor_vel, r_vel, self._right_motor_vel, heading))
        self.set_left_motor(l_vel)
        self.set_right_motor(r_vel)
        self.headings.append(heading)
        self.desired_angles.append(desired_angle)
        self.xs.append(x)
        self.ys.append(y)
        return


    def get_desired_angle(self, x, y):
        next_cell = self.dfs.get_next_cell(x, y)
        arctan = math.atan2(next_cell[1] - y, next_cell[0] - x)
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
        print('Number iterations in final run: {:,}'.format(len(self.xs) - self.race_start))
        plt.subplot(1, 2, 1)
        plt.plot(range(len(self.headings)), self.headings)
        plt.plot(range(len(self.desired_angles)), self.desired_angles)

        plt.subplot(1, 2, 2)
        plt.plot(self.xs[:self.race_start], self.ys[:self.race_start], color='lightblue')
        plt.plot(self.xs[self.race_start:], self.ys[self.race_start:], color='midnightblue')
        for y in range(len(self.maze.maze)):
            print(y)
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

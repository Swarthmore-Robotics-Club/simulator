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
        self.set_right_motor(0)
        self.set_left_motor(0)
        self.pid = PIDLoop(0.065, 0, 0.05)
        self.state = 0
        self.maze = maze
        self.goal = self.maze.get_goal()
        self.next_cell = None
        self.already_visited = set()

        # next 2 lines are hacky way to set the initial position appropriately
        # don't want to set in Robot.py because that screws up earlier bots
        self._x = 0.5
        self._y = 0.5


        self.headings = []
        self.desired_angles = []
        self.xs = []
        self.ys = []
        return

    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        if x < -1 or y < -1 or y > self.maze._max_y + 2 or x > self.maze._max_x + 2:
            raise Exception('x: {}, y: {}'.format(x, y))
        heading = self.get_heading()
        desired_angle = self.get_desired_angle(x, y)
        self.headings.append(heading)
        self.desired_angles.append(desired_angle)
        self.xs.append(x)
        self.ys.append(y)
        return

    def get_desired_angle(self, x, y):
        if self.next_cell:
            acceptable_offset = 0.05
            desired_x = self.next_cell[0]
            desired_y = self.next_cell[1]
            if desired_x - acceptable_offset <= x <= desired_x + acceptable_offset:
                if desired_y - acceptable_offset <= y <= desired_y + acceptable_offset:
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
            print(self.next_cell)
        arctan = math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)
        if arctan < 0:
            arctan += TWO_PI
        return arctan


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

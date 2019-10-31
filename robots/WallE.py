import math
import matplotlib.pyplot as plt
from PIDLoop import PIDLoop
from Robot import Robot

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
        heading = self.get_heading()
        desired_angle = self.get_desired_angle(x, y)

        self.headings.append(heading)
        self.desired_angles.append(desired_angle)
        self.xs.append(x)
        self.ys.append(y)
        return

    def get_desired_angle(self, x, y):
        return math.pi / 2

    def print_graphs(self):
        fig = plt.figure()

        plt.subplot(1, 2, 1)
        plt.plot(range(len(self.headings)), self.headings)
        plt.plot(range(len(self.desired_angles)), self.desired_angles)

        plt.subplot(1, 2, 2)
        plt.plot(self.xs, self.ys)

        n = len(self.maze.maze)
        for x in range(n):
            for y in range(n):
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

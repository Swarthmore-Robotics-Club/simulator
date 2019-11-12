import math
# import matplotlib.pyplot as plt
from DFS import DFS
from PIDLoop import PIDLoop
from Robot import Robot

TWO_PI = 2 * math.pi

class TheVisibleHand(Robot):
    def __init__(self, maze):
        Robot.__init__(self)
        self.maze = maze
        self.xs = []
        self.ys = []

        # next 2 lines are hacky way to set the initial position appropriately
        # don't want to set in Robot.py because that screws up earlier bots
        self._x = 0.5
        self._y = 0.5
        return


    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        if x < -1 or y < -1 or y > self.maze._max_y + 2 or x > self.maze._max_x + 2:
            raise Exception('x: {}, y: {}'.format(x, y))
        heading = self.get_heading()
        if heading > math.pi:
            heading -= TWO_PI

        return



    def print_graphs(self):
        return
    
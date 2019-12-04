import math
import random
from mazes.Labyrinth import Labyrinth, DARK_BLUE
from mazes.MazeGenerator import MazeGenerator
from utils.DFSL import DFSL
from utils.PIDLoop import PIDLoop
from utils.StateL import ThePartyL
from Robot import Robot

LENGTH_OF_MAZE = 16
STARTING_LOCATION = (0.5, 0.5)

# random.seed(0)

class AMEE(Robot):
    def __init__(self):
        Robot.__init__(self)
        self._x, self._y = STARTING_LOCATION
        self.labyrinth = Labyrinth(MazeGenerator(LENGTH_OF_MAZE, LENGTH_OF_MAZE).maze, LENGTH_OF_MAZE * 50, LENGTH_OF_MAZE * 50, 50)
        self.usa = ThePartyL(self.labyrinth, self.set_race_start)
        self.xs = []
        self.ys = []
        self.race_start = 30
        return


    def set_race_start(self):
        self.race_start = len(self.xs)
        return


    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        heading = self.get_heading()
        l_vel, r_vel = self.usa.get_velocities(x, y, heading, dt) 
        self.set_right_motor(r_vel)
        self.set_left_motor(l_vel)
        self.xs.append(x)
        self.ys.append(y)
        return


    def print_graphs(self):
        self.labyrinth.draw_lines(self.xs[:self.race_start], self.ys[:self.race_start])
        self.labyrinth.draw_lines(self.xs[self.race_start:], self.ys[self.race_start:], DARK_BLUE)
        self.labyrinth.display()
        return
import math
import random
from mazes.Labyrinth import Labyrinth
from mazes.MazeGenerator import MazeGenerator
from utils.DFSL import DFSL
from utils.PIDLoop import PIDLoop
from utils.StateL import ThePartyL
from Robot import Robot

LENGTH_OF_MAZE = 16
STARTING_LOCATION = (0.5, 0.5)

random.seed(0)

class AMEE(Robot):
    def __init__(self):
        Robot.__init__(self)
        self._x, self._y = STARTING_LOCATION
        self.labyrinth = Labyrinth(MazeGenerator(LENGTH_OF_MAZE, LENGTH_OF_MAZE).maze)
        self.usa = ThePartyL(self.labyrinth, self.set_race_start, self, STARTING_LOCATION)
        self.xs = []
        self.determined_xs = []
        self.ys = []
        self.determined_ys = []
        self.race_start = 0
        return


    def set_race_start(self):
        self.race_start = len(self.xs)
        return


    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        heading = self.get_heading()
        # print('reality: {}'.format(tuple(map(lambda x: round(x, 4), (x, y, heading)))))
        l_vel, r_vel = self.usa.get_velocities(x, y, heading, dt)
        self.set_right_motor(r_vel)
        self.set_left_motor(l_vel)
        # print('left vel: {}, right vel: {}'.format(l_vel, r_vel))
        self.determined_xs.append(self.usa.position[0])
        self.xs.append(x)
        self.determined_ys.append(self.usa.position[1])
        self.ys.append(y)
        return


    def print_graphs(self):
        self.labyrinth.draw_lines(self.xs[:self.race_start], self.ys[:self.race_start], 'lightblue')
        self.labyrinth.draw_lines(self.xs[self.race_start:], self.ys[self.race_start:], 'midnightblue')
        self.labyrinth.draw_lines(self.determined_xs[:self.race_start], self.determined_ys[:self.race_start], 'salmon')
        self.labyrinth.draw_lines(self.determined_xs[self.race_start:], self.determined_ys[self.race_start:], 'red')
        self.labyrinth.display()
        return

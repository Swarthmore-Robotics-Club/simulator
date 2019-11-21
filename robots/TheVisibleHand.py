import math
import matplotlib.pyplot as plt
from robots.DFS import DFS
from robots.PIDLoop import PIDLoop
from robots.Robot import Robot
from robots.State import TheParty

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
        self.peoples_liberation_front = TheParty(maze)
        return


    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        if x < -1 or y < -1 or y > self.maze._max_y + 2 or x > self.maze._max_x + 2:
            raise Exception('x: {}, y: {}'.format(x, y))
        heading = self.get_heading()

        # now use our state to ask the Party what to do
        l_vel, r_vel = self.peoples_liberation_front.get_velocities(x, y, heading, dt) 
        self.set_right_motor(r_vel)
        self.set_left_motor(l_vel)
        
        # print('desired left wheel vel: {:2.4}, actual left wheel vel {:2.4}, desired right wheel vel: {:2.4}, actual right wheel vel {:2.4}, heading: {:2.4} '.format(l_vel, self._left_motor_vel, r_vel, self._right_motor_vel, heading))
        self.xs.append(x)
        self.ys.append(y)
        return

   
    def print_graphs(self):
        fig = plt.figure()
        plt.plot(self.xs, self.ys, color='lightblue')
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
    
from mazes.BottomLeftMaze import BottomLeftMaze
from PIDLoop import PIDLoop
from robot import Robot

"""
starts at 0,0 facing East. Wants to check where it can go. Goal is at 2,0
"""
class WallE(Robot):
    def __init__(self, path):
        Robot.__init__(self)
        self.set_right_motor(0)
        self.set_left_motor(0)
        self.pid = PIDLoop(0.065, 0, 0.05)
        self.state = 0
        self.maze = BottomLeftMaze(path)
        return

    def loop(self, dt):
        return

    def print_graphs(self):
        return

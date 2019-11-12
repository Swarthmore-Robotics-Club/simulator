import sys
sys.path.append('robots')
sys.path.append('mazes')
from mazes.Maze import Maze
from robots.WallE import WallE
from robots.TheVisibleHand import TheVisibleHand

maze = Maze(sys.argv[1] if len(sys.argv) > 1 else 'mazes/data/example1.map')
robot = TheVisibleHand(maze)
dt = 0.01

try:
    j = 0
    while True:
        j += 1
        robot.loop(dt)
        robot._integrate_motors(dt)
except (Exception, KeyboardInterrupt) as e:
    print('\n\n', e, '\n\nj: {:,}'.format(j))

robot.print_graphs()

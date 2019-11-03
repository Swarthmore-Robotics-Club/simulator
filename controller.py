import sys
sys.path.append('robots')
sys.path.append('mazes')
from mazes.BottomLeftMaze import BottomLeftMaze
from WallE import WallE

maze = BottomLeftMaze(sys.argv[1] if len(sys.argv) > 1 else 'mazes/data/example1.map')
robot = WallE(maze)
dt = 0.01

try:
    j = 0
    for i in range(8000):
        j += 1
        robot.loop(dt)
        robot._integrate_motors(dt)
        print(j)
except (Exception, KeyboardInterrupt) as e:
    print('\n\n\n', e, '\n\n\n', j)

robot.print_graphs()

import logging
import sys
sys.path.append('robots')
sys.path.append('mazes')
sys.path.append('utils')
from mazes.Maze import Maze
from robots.AMEE import AMEE


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# maze = Maze(sys.argv[1] if len(sys.argv) > 1 else 'mazes/data/example1.map')
robot = AMEE()
dt = 0.01

j = 0
try:
    while True:
        j += 1
        robot.loop(dt)
        robot._integrate_motors(dt)
except (Exception, KeyboardInterrupt) as e:
    logger.exception(e)
print('\n\nj: {:,}'.format(j))
robot.print_graphs()

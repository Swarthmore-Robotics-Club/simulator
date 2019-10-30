import sys
sys.path.append('robots')
from OptimusPrime import OptimusPrime


robot = OptimusPrime()
dt = 0.01
try:
    j = 0
    for i in range(2000):
        j += 1
        robot.loop(dt)
        robot._integrate_motors(dt)
except (Exception, KeyboardInterrupt) as e:
    print('\n\n\n', e, '\n\n\n', j)

robot.print_graphs()
    
import math
import matplotlib.pyplot as plt
from PIDLoop import PIDLoop
from Robot import Robot

TWO_PI = 2 * math.pi

"""
Starts at 0,0, facing East. Wants to go 3 units North, 2 units East, 3 units South.
"""
class OptimusPrime(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.set_right_motor(0)
        self.set_left_motor(0)
        self.pid = PIDLoop(0.065, 0, 0.05)
        self.state = 0

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
        pid_result = self.pid.updateError(desired_angle - heading, dt)
        pid_result_proportion = pid_result / TWO_PI
        if pid_result > 0.001:
            self.set_right_motor(self._right_motor - pid_result_proportion)
            self.set_left_motor(self._left_motor + pid_result_proportion)
        elif pid_result < -0.001:
            self.set_left_motor(self._left_motor + pid_result_proportion)
            self.set_right_motor(self._right_motor + abs(pid_result_proportion))
        else:
            self.set_left_motor(1.0)
            self.set_right_motor(1.0)

        self.headings.append(heading)
        self.desired_angles.append(desired_angle)
        self.xs.append(x)
        self.ys.append(y)
        return


    def get_desired_angle(self, x, y):
        if x < 1 and y <= 2: # starting, go up
            return math.pi / 2
        elif x < 1.5: # go right
            if self.state == 0:
                self.state = 1
                self.set_left_motor(0)
                self.set_right_motor(0)
            return 0
        elif x >= 1.5 and y > 0: # go down
            if self.state == 1:
                self.state = 2
                self.set_left_motor(0)
                self.set_right_motor(0)
            return 1.5 * math.pi
        raise Exception('We done here.')


    def print_graphs(self):
        fig = plt.figure()

        plt.subplot(1, 2, 1)
        plt.plot(range(len(self.headings)), self.headings)
        plt.plot(range(len(self.desired_angles)), self.desired_angles)

        plt.subplot(1, 2, 2)
        plt.plot(self.xs, self.ys)
        plt.plot([0.4, 0.4, 1.6, 1.6], [0, 2.6, 2.6, 0], color='gray') # inner wall
        plt.plot([-0.1, -0.1, 2.1, 2.1], [0, 3.1, 3.1, 0], color='gray') # outer wall

        plt.show()
        return

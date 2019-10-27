import robot as rb
import math
import matplotlib.pyplot as plt
import numpy as np


TWO_PI = 2 * math.pi
headings = []
xs = []
ys = []
pids = []
desired_angles = []

class ExampleRobot(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0.5)
        self.set_left_motor(-0.1)

    def loop(self, dt):
        print('x: {}, y: {}, heading: {}'.format(self.get_x(), self.get_y(), self.get_heading()))


"""
Goes straight. Yay.
"""
class StraightAsASpaghetti(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0)
        self.set_left_motor(0)
        return
    
    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        heading = self.get_heading()
        self.set_right_motor(1)
        self.set_left_motor(1)
        print('x: {:2.4}, y: {:2.4}, heading: {:2.4}'.format(x, y, heading))
        return


"""
Starts at 0,0, facing East. Wants to go 3 units North, 2 units East, 3 units South.
"""
class OptimusPrime(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0)
        self.set_left_motor(0)
        self.pid = PIDLoop(0.065, 0, 0.05)
        self.state = 0
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

        global pids, headings, xs, ys, desired_angles
        pids.append(pid_result)
        headings.append(heading)
        xs.append(x)
        ys.append(y)
        desired_angles.append(desired_angle)
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


class PIDLoop():
    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.p_error = 0
        self.i_error = 0
        self.d_error = 0
        return
    
    def updateError(self, error, dt):
        old_error = self.p_error
        self.p_error = error
        self.i_error = (self.i_error + error * dt) if error != 0 else 0
        self.d_error = (error - old_error) / dt
        return -self.kP * self.p_error - self.kI * self.i_error - self.kD * self.d_error


if __name__ == '__main__':
    world = rb.World(OptimusPrime())

    try:
        j = 0
        for i in range(2000):
            j += 1
            world.loop(0.01)
    except (Exception, KeyboardInterrupt) as e:
        print('\n\n\n', e, '\n\n\n', j)
    
    fig = plt.figure()

    plt.subplot(1, 2, 1)
    plt.plot(range(len(headings)), headings)
    plt.plot(range(len(desired_angles)), desired_angles)

    plt.subplot(1, 2, 2)
    plt.plot(xs, ys)
    plt.plot([0.4, 0.4, 1.6, 1.6], [0, 2.6, 2.6, 0], color='gray') # inner wall
    plt.plot([-0.1, -0.1, 2.1, 2.1], [0, 3.1, 3.1, 0], color='gray') # outer wall

    plt.show()

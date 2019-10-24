import robot as rb
import math

TWO_PI = 2 * math.pi

class ExampleRobot(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0.5)
        self.set_left_motor(-0.1)

    def loop(self, dt):
        print('x: {}, y: {}, heading: {}'.format(self.get_x(), self.get_y(), self.get_heading()))

"""
Starts at 0,0, facing East. Wants to go 3 units North, 2 units East, 3 units South.
"""
class OptimusPrime(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0)
        self.set_left_motor(0)
        self.last_error = 0
        return


    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        heading = self.get_heading()
        desired_angle = self.get_desired_angle(x, y)
        pid_result = self.angle_PID_loop(desired_angle, heading, dt)
        pid_result_proportion = pid_result / TWO_PI
        if pid_result > 0:
            self.set_right_motor(pid_result_proportion)
            self.set_left_motor(0 - pid_result_proportion)
        elif pid_result < 0:
            self.set_left_motor(0 - pid_result_proportion)
            self.set_right_motor(pid_result_proportion)
        else:
            self.set_left_motor(1)
            self.set_right_motor(1)
        print('pid: {:2.4}, x: {:2.4}, y: {:2.4}, heading: {:2.4}'.format(pid_result, x, y, heading))
        return


    def get_desired_angle(self, x, y):
        if x < 1 and y < 2: # starting
            return math.pi / 2
        return 0


    def angle_PID_loop(self, goal_angle, current_angle, dt):
        proportional_gain = 1
        derivative_gain = 1
        e_of_t = goal_angle - current_angle
        print(e_of_t)
        derivative = (e_of_t - self.last_error) * dt
        self.last_error = e_of_t
        return proportional_gain * e_of_t + derivative_gain * derivative


if __name__ == '__main__':
    world = rb.World(OptimusPrime())

    for i in range(100):
        world.loop(0.01)

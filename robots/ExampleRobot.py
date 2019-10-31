import Robot as rb

class ExampleRobot(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0.5)
        self.set_left_motor(-0.1)

    def loop(self, dt):
        print('x: {}, y: {}, heading: {}'.format(self.get_x(), self.get_y(), self.get_heading()))
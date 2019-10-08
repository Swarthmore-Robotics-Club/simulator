import robot as rb

class ExampleRobot(rb.Robot):
    def __init__(self):
        rb.Robot.__init__(self)
        self.set_right_motor(0.5)
        self.set_left_motor(-0.1)

    def loop(self, dt):
        print(self.get_x(), self.get_y(), self.get_heading())

if __name__ == '__main__':
    world = rb.World(ExampleRobot())

    for i in range(100):
        world.loop(0.01)

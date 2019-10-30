from robot import Robot

"""
Goes straight. Yay.
"""
class StraightAsASpaghetti(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.set_right_motor(1)
        self.set_left_motor(1)
        return
    
    def loop(self, dt):
        x = self.get_x()
        y = self.get_y()
        heading = self.get_heading()
        print('x: {:2.4}, y: {:2.4}, heading: {:2.4}'.format(x, y, heading))
        return


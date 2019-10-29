import sys
sys.path.append('..')
import robot as rb 

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


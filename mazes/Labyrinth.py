import math
import matplotlib.pyplot as plt

TWO_PI = 2 * math.pi
HALF_PI = math.pi / 2

class Labyrinth():
    def __init__(self, maze, screen_width = 800, screen_height = 800, screen_cell_width = 50):
        self.maze = maze # assumed maze similar style as generated by MazeGenerator class
        self.width = screen_width
        self.height = screen_height
        self.cell_width = screen_cell_width
        self._max_x = len(self.maze[0]) - 1
        self._max_y = len(self.maze) - 1
        return


    def get_goal(self):
        return (self._max_x + 0.5, self._max_y + 0.5)


    # returns distance to nearest wall from each sensor (w/ 1 being the width of a cell) or float('inf') if the wall's too far
    def get_sensor_readings(self, x1, y1, heading, root = True):
        BIG_DIAMETER = 16 * math.sqrt(2)
        x2 = x1 + BIG_DIAMETER*math.cos(heading)
        y2 = y1 + BIG_DIAMETER*math.sin(heading)
        form_for_y = lambda x: y1 + ((y2 - y1) * (x - x1)/(x2 - x1))
        form_for_x = lambda y: x1 + ((x2 - x1) * (y - y1)/(y2 - y1))
        potential_walls = []
        for x in self._generate_ints_between(x1, x2):
            y = form_for_y(x)
            potential_walls.append((x, y, math.hypot(x - x1, y - y1)))
        for y in self._generate_ints_between(y1, y2):
            x = form_for_x(y)
            potential_walls.append((x, y, math.hypot(x - x1, y - y1)))
        potential_walls = sorted(potential_walls, key=lambda pt: pt[2])
        straight = float('inf')
        for possible in potential_walls:
            if self._is_wall(possible[0], possible[1]):
                straight = possible[2]
                break
        if not root:
            return straight
        left = self.get_sensor_readings(x1, y1, self._rescale_heading(heading + HALF_PI), False)
        right = self.get_sensor_readings(x1, y1, self._rescale_heading(heading - HALF_PI), False)
        return (straight, left, right)


    def _rescale_heading(self, heading):
        if heading < -math.pi:
            return heading + TWO_PI
        if heading > math.pi:
            return heading - TWO_PI
        return heading


    def _generate_ints_between(self, x1, x2):
        big = max(x1, x2)
        small = min(x1, x2)
        if isinstance(big, int):
            return range(math.ceil(small), big + 1)
        return range(math.ceil(small), math.ceil(big))


    def _is_wall(self, x, y):
        if isinstance(x, int): # means we're on a vertical line
            if x >= len(self.maze[0]):
                return True
            if isinstance(y, int): # means we're at a corner
                return True in self.maze[y][x].walls[2:] # check if either down or left is a wall
            return self.maze[math.floor(y)][x].walls[3]
        if isinstance(y, int): # horizontal line
            if y >= len(self.maze):
                return True # always a wall boi
            return self.maze[y][math.floor(x)].walls[2]
        return False # as we're not on a line, can't be at a wall


    def draw_lines(self, xs, ys, color='lightblue'):
        plt.plot(xs, ys, color=color)
        return
    

    def display(self):
        for row in self.maze:
            for cell in row:
                self._draw_maze_cell(cell)
        plt.show()
        return


    def _draw_maze_cell(self, maze_cell):
        x = maze_cell.x
        y = maze_cell.y
        if maze_cell.walls[0]:
            plt.plot([x, x + 1], [y + 1, y + 1], color='gray')
        if maze_cell.walls[1]:
            plt.plot([x + 1, x + 1], [y, y + 1], color='gray')
        if maze_cell.walls[2]:
            plt.plot([x, x + 1], [y, y], color='gray')
        if maze_cell.walls[3]:
            plt.plot([x, x], [y, y + 1], color='gray')
        return


if __name__ == '__main__':
    from random import seed
    from MazeGenerator import MazeGenerator

    seed(0)
    width = 800
    height = 800
    cell_width = 50
    cols = width // cell_width
    rows = height // cell_width
    gen = MazeGenerator(rows, cols)
    wicked = Labyrinth(gen.maze, width, height, cell_width)
    print(wicked.get_sensor_readings(0.5, 0.5, HALF_PI + .2))
    xs = [x/10 for x in range(5, 40)]
    ys = [y/10 for y in range(5, 40)]
    wicked.draw_lines(xs, ys)
    wicked.display()

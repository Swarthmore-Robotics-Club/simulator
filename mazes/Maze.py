OPEN_CELL = '.'
WALL = '#'

"""
0,0 is bottom left, goal is top right
"""
class Maze():
    def __init__(self, path):
        with open(path) as f:
            self.maze =  [ [ cell for cell in row.rstrip() ] for row in f ]
            self.maze = self.maze[::-1]
        self._max_x = len(self.maze[0]) - 1
        self._max_y = len(self.maze) - 1
        return

    def can_up(self, x, y):
        if x < 0 or x > self._max_x or y < 0 or y > (self._max_y - 1):
            return False
        return self.maze[y + 1][x] == OPEN_CELL

    def can_left(self, x, y):
        if x < 1 or x > self._max_x or y < 0 or y > self._max_y:
            return False
        return self.maze[y][x - 1] == OPEN_CELL

    def can_right(self, x, y):
        if x < 0 or x > (self._max_x - 1) or y < 0 or y > self._max_y:
            return False
        return self.maze[y][x + 1] == OPEN_CELL

    def can_down(self, x, y):
        if x < 0 or x > self._max_x or y < 1 or y > self._max_y:
            return False
        return self.maze[y - 1][x] == OPEN_CELL

    def get_goal(self):
        return (self._max_x + 0.5, self._max_y + 0.5)

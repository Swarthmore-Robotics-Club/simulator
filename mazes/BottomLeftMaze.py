from Maze import Maze

OPEN_CELL = '.'
WALL = '#'

class BottomLeftMaze(Maze):
    def __init__(self, path):
        Maze.__init__(self)
        with open(path) as f:
            self.maze =  [ [ cell for cell in row.rstrip() ] for row in f ]
            self.maze = self.maze[::-1]
        return


    def can_up(self, x, y):
        try:
            return self.maze[x][y-1] == OPEN_CELL
        except:
            return False


    def can_left(self, x, y):
        try:
            return self.maze[x-1][y] == OPEN_CELL
        except:
            return False


    def can_right(self, x, y):
        try:
            return self.maze[x+1][y] == OPEN_CELL
        except:
            return False


    def can_down(self, x, y):
        try:
            return self.maze[x][y + 1] == OPEN_CELL
        except:
            return False

class Maze():
    def __init__(self, path):
        self.maze = []


class BottomLeftMaze(Maze):

    def __init__(self,path):
        """
            Given a file path, creates a maze
        """

        with open(path) as f:
            self.maze =  [ [(cell) for cell in row.rstrip()] for row in  f  ]

            self.maze = self.maze[::-1]
            
    def can_up(self, x, y):
        try:
            val = self.maze[x][y-1]
            return val == "#"
        except:
            return False
    
    def can_left(self, x, y):
        try:
            val = self.maze[x-1][y]
            return val == "#"
        except:
            return False


    def can_right(self, x, y):
        try:
            val = self.maze[x+1][y]
            return val == "#"
        except:
            return False

    def can_down(self, x, y):
        try:
            val = self.maze[x][y + 1]
            return val == "#"
        except:
            return False

"""
    The maze generator will randomly create a maze and output its corresponding 
    JSON interpretation of the maze
"""

class MazeCell():
    def _init__(self, maze):
        self.visited = False
        self.walls = [1, 1, 1, 1]
        self.maze = maze
        self.visited = False

    
    def get_neighbors(self):
        pass


    def to_json(self):
        pass
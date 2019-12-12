"""
    The maze generator will randomly create a maze and output its corresponding 
    JSON interpretation of the maze
"""
import random 
import json

class MazeCell():
    def __init__(self, x, y):
        self.y = y
        self.x = x
        self.walls = [True, True, True, True] # order of walls is Top, Right, Bottom, Left
        self.visited = False
        return


    def to_json(self):
        return {
            'x': self.x,
            'y': self.y,
            'walls': self.walls
        }


    def __repr__(self):
        return str(self.to_json())


class MazeGenerator():
    def __init__(self, rows, cols):
        self.maze = [[MazeCell(c, r) for c in range(cols)] for r in range(rows)]
        self.generate_maze()

        for row in self.maze:
            for cell in row:
                # god forgive me
                cell.walls[0], cell.walls[2] =  cell.walls[2], cell.walls[0]
                # cell.walls[1], cell.walls[3] =  cell.walls[3], cell.walls[1]

        self.set_goal()

        return
    def set_goal(self):
        
        top_left_x = random.randint(4, len(self.maze[0]) -4)
        top_left_y = random.randint(4, len(self.maze) -4)

        top_left_cell = self.maze[top_left_y][top_left_x]

        top_right_cell = self.maze[top_left_y][top_left_x+ 1]

        self.remove_walls(top_left_cell, top_right_cell)

        bottom_right_cell = self.maze[top_left_y-1][top_left_x+ 1]

        self.remove_walls(top_right_cell, bottom_right_cell)

        bottom_left_cell = self.maze[top_left_y-1][top_left_x]

        self.remove_walls(top_right_cell, bottom_left_cell)
        self.remove_walls(bottom_left_cell, bottom_right_cell)

        self.goal = (top_right_cell.x, top_right_cell.y)





        
        



    def generate_maze(self):
        """
        randomly generates a maze using a recursive backtracker as specified by
        https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker
        """
        stack = []
        start = self.maze[0][0]
        start.visited = True
        curr_cell = None
        stack.append(start)

        while stack:
            if curr_cell == None:
                curr_cell = stack.pop()
            
            neighbor = self.get_unvisited_neighbor(curr_cell)
            if neighbor:
                neighbor.visited = True
                stack.append(curr_cell) # push curr to stack for backtracking
                self.remove_walls(curr_cell, neighbor)
            curr_cell = neighbor
        return


    def get_unvisited_neighbor(self, cell):
        neighbors = []
        x = cell.x
        y = cell.y
        if x - 1 >= 0 and not self.maze[y][x - 1].visited: # left
            neighbors.append(self.maze[y][x - 1])
        if y - 1 >= 0 and not self.maze[y - 1][x].visited: # top
            neighbors.append(self.maze[y - 1][x])
        if x + 1 < len(self.maze) and not self.maze[y][x + 1].visited: # right
            neighbors.append(self.maze[y][x + 1])
        if y + 1 < len(self.maze[0]) and not self.maze[y + 1][x].visited: # bottom
            neighbors.append(self.maze[y + 1][x])

        if neighbors:
            return random.choice(neighbors)
        return None


    def remove_walls(self, cell, neighbor_cell):
        x = cell.x - neighbor_cell.x
        y = cell.y - neighbor_cell.y
        if x == 1: # neighbor is to the left 
            cell.walls[3] = False
            neighbor_cell.walls[1] = False
        elif x == -1: # neighbor is to the right
            cell.walls[1] = False
            neighbor_cell.walls[3] = False
        if y == 1: # neighbor is above
            cell.walls[0] = False
            neighbor_cell.walls[2] = False
        elif y == -1: # neighbor is below
            cell.walls[2] = False
            neighbor_cell.walls[0] = False
        return 


    def to_json(self):
        return { 'cells': [ cell.to_json() for row in self.maze for cell in row ] }

    
    def write(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.to_json(), outfile, indent=3)
        return

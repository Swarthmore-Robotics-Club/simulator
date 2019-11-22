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
        self.visited = False
        # 1 if there is a wall 0 if there is not a wall 
        self.walls = [1, 1, 1, 1] # order of walls is Top, Right, Bottom, Left
        self.visited = False

    
    def get_rand_neighbor(self, maze):
        """
        returns a random neighbor as long as it is valid in the maze
        and it has not been visited before

        if no valid neighbors exist return None
        """

        neighbors = []
        # left
        if self.x - 1 >= 0 and not maze[self.y][self.x - 1].visited:
            neighbors.append(maze[self.y][self.x - 1])
        # top
        if self.y - 1 >= 0 and not maze[self.y - 1][self.x].visited:
            neighbors.append(maze[self.y - 1][self.x])
        # right
        if self.x + 1 < len(maze) and not maze[self.y][self.x + 1].visited:
            neighbors.append(maze[self.y][self.x + 1])
        # bottom
        if self.y + 1 < len(maze[0]) and not maze[self.y - 1][self.x].visited:
            neighbors.append(maze[self.y - 1][self.x])

        if neighbors:
            return neighbors[random.randint(0, len(neighbors) - 1)] 
        else:
            return None

    def to_json(self):

        return {
            "x": self.x,
            "y" : self.y,
            "walls" : self.walls
        }
        

    
class MazeGenerator():
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols 
        self.maze = [ [MazeCell(r, c) for c in range(cols)] for r in range(rows)   ]
        # self.maze = self.maze[::-1]
        self.json = None
        self.generate_maze()
        

        print("all done here")

    def regen(self, rows, cols):
        """
        Regenerates a new MxN maze with new dimensions instead of having to create new class instance
        """
        self.__init__(rows, cols)

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
            if not curr_cell:
                curr_cell = stack.pop()
            
            neighbor = curr_cell.get_rand_neighbor(self.maze)
            if neighbor:
                neighbor.visited = True

                # push curr to stack for backtracking
                stack.append(curr_cell)
                self.remove_walls(curr_cell, neighbor)
                curr_cell = neighbor
            else:
                curr_cell = None
        self.json = self.to_json()
            


    def remove_walls(self, cell, neighbor_cell):
        x = cell.x - neighbor_cell.x
        y = cell.y - neighbor_cell.y

        if x == 1:
            # if the neihbor is to the left 
            cell.walls[3] = 0 
            neighbor_cell.walls[1] = 0
        elif x == -1:
            # if neighbor is to the riight
            cell.walls[1] = 0 
            neighbor_cell.walls[3] = 0
        if y == 1:
            # if neighbor is above cell
            cell.walls[0] = 0 
            neighbor_cell.walls[2] = 0
        elif y == -1:
            # if neighbor is below cell
            cell.walls[2] = 0 
            neighbor_cell.walls[0] = 0

    def to_json(self):
        return  {
            "rows" : self.rows,
            "cols" : self.cols,
            "cells" : [ cell.to_json() for row in self.maze for cell in row ]
        }
    def write(self, filename, path = ""):
        """
            writes the json interpretation of the maze to a file
        """
        with open(filename, 'w') as outfile:
            json.dump(self.json, outfile, indent=3)
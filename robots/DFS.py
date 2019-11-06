from collections import defaultdict
import math

class DFS():
    def __init__(self, maze, goal, acceptable_offset=0.1, starting_loc=(0.5, 0.5)):
        self.goal = goal
        self.maze = maze
        self.acceptable_offset = acceptable_offset
        self.already_visited = set([starting_loc])
        self.graph = defaultdict(set)
        self.stack = []
        self.next_cell = None # tuple
        return
    
    
    def add_current_cell(self, current):
        neighbors = []
        x, y = current
        floor_x = math.floor(x)
        floor_y = math.floor(y)
        if self.maze.can_left(floor_x, floor_y):
            neighbors.append((x - 1, y))
        if self.maze.can_down(floor_x, floor_y):
            neighbors.append((x, y - 1))
        if self.maze.can_right(floor_x, floor_y):
            neighbors.append((x + 1, y))
        if self.maze.can_up(floor_x, floor_y):
            neighbors.append((x, y + 1))
        for bor in neighbors:
            self.graph[current].add(bor)
            if bor not in self.already_visited:
                self.already_visited.add(bor)
                self.stack.append(bor)
        return
    
    
    def get_next_cell(self, x, y):
        if not self.next_cell: # assume idealized start
            self.add_current_cell((x, y))
            self.next_cell = self.stack.pop()
        desired_x, desired_y = self.next_cell
        if abs(desired_x - x) > self.acceptable_offset or abs(desired_y - y) > self.acceptable_offset:
            return self.next_cell
        if desired_x == self.goal[0] and desired_y == self.goal[1]:
            raise Exception('We done here', self.goal, x, y)
        self.add_current_cell(self.next_cell)
        if len(self.stack) == 0:
            raise Exception('We had an empty stack but hadn\'t hit goal yet', x, y, '\n\n', self.graph)

        if not self.is_adjacent(self.next_cell, self.stack[-1]):
            p = self.find_shortest_path(self.next_cell, self.stack[-1])[::-1]
            p = p[1:-1]
            self.stack.extend(p)
        self.next_cell = self.stack.pop()
        return self.next_cell


    def is_adjacent(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1


    def find_shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        shortest = None
        for node in self.graph[start]:
            if node not in path:
                newpath = self.find_shortest_path(node, end, path)
                if newpath and (not shortest or len(newpath) < len(shortest)):
                    shortest = newpath
        return shortest
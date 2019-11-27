from collections import defaultdict, deque
import math

class DFS():
    def __init__(self, maze, goal, callback, acceptable_offset=0.1, starting_loc=(0.5, 0.5)):
        self.goal = goal
        self.maze = maze
        self.callback = callback
        self.acceptable_offset = acceptable_offset
        self.already_visited = set([starting_loc])
        self.graph = defaultdict(set)
        self.stack = []
        self.next_cell = None # tuple
        self.state = 0
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
        if self.state == 2 and desired_x == self.goal[0] and desired_y == self.goal[1]:
            raise Exception('We done here', self.goal, x, y)
        self.add_current_cell(self.next_cell)
        if len(self.stack) == 0:
            if self.state == 0:
                self.stack.append((0.5, 0.5))
                self.state = 1
            elif self.state == 1:
                self.stack.append(self.goal)
                self.callback()
                self.state = 2
            else:
                raise Exception('We had an empty stack but hadn\'t finished yet', x, y, '\n\n', self.graph)

        if not self.is_adjacent(self.next_cell, self.stack[-1]):
            p = self.find_shortest_path(self.next_cell, self.stack[-1])[::-1]
            p = p[1:-1]
            self.stack.extend(p)
        self.next_cell = self.stack.pop()
        return self.next_cell


    def is_adjacent(self, p1, p2):
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) == 1


    def find_shortest_path(self, start, end):
        nodes_to_visit = {start}
        visited_nodes = set()
        distance_from_start = defaultdict(lambda: float('inf'))
        distance_from_start[start] = 0
        tentative_parents = {}

        while nodes_to_visit:
            current = min([(distance_from_start[node], node) for node in nodes_to_visit])[1]
            if current == end:
                break

            nodes_to_visit.discard(current)
            visited_nodes.add(current)

            for neighbour in self.graph[current]:
                if neighbour in visited_nodes:
                    continue
                neighbour_distance = distance_from_start[current] + 1
                if neighbour_distance < distance_from_start[neighbour]:
                    distance_from_start[neighbour] = neighbour_distance
                    tentative_parents[neighbour] = current
                    nodes_to_visit.add(neighbour)

        return self._deconstruct_path(tentative_parents, end)


    def _deconstruct_path(self, tentative_parents, end):
        if end not in tentative_parents:
            return None
        cursor = end
        path = []
        while cursor:
            path.append(cursor)
            cursor = tentative_parents.get(cursor)
        return list(reversed(path))

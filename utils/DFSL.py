from collections import defaultdict
import math

def tp(t, n = 4):
    return tuple(map(lambda x: round(x, n), t))

class DFSL():
    def __init__(self, labyrinth, goal, callback, acceptable_offset=0.1, starting_loc=(0.5, 0.5)):
        self.goal = goal
        self.labyrinth = labyrinth
        self.callback = callback
        self.acceptable_offset = acceptable_offset
        self.starting_location = starting_loc
        self.already_visited = set([starting_loc])
        self.graph = defaultdict(set)
        self.stack = []
        self.next_cell = None # tuple
        self.state = 0
        self.distance_threshold = .8
        return


    def add_current_cell(self, determined_current, real_current, heading):
        neighbors = []
        straight, left, right = self.labyrinth.get_sensor_readings(*real_current, heading)
        print('sensors: {}, heading: {}'.format(tp((straight, left, right)), tp((heading,))[0]))
        x, y = determined_current
        exact_x = math.floor(x) + .5
        exact_y = math.floor(y) + .5
        if heading < math.pi / 4 or heading > 1.75 * math.pi: # straight ahead is right
            if straight > self.distance_threshold:
                neighbors.append((exact_x + 1, exact_y))
            if left > self.distance_threshold:
                neighbors.append((exact_x, exact_y + 1))
            if right > self.distance_threshold:
                neighbors.append((exact_x, exact_y - 1))
        elif heading < .75 * math.pi: # straight ahead is up
            if straight > self.distance_threshold:
                neighbors.append((exact_x, exact_y + 1))
            if left > self.distance_threshold:
                neighbors.append((exact_x - 1, exact_y))
            if right > self.distance_threshold:
                neighbors.append((exact_x + 1, exact_y))
        elif heading < 1.25 * math.pi: # straight ahead is left
            if straight > self.distance_threshold:
                neighbors.append((exact_x - 1, exact_y))
            if left > self.distance_threshold:
                neighbors.append((exact_x, exact_y - 1))
            if right > self.distance_threshold:
                neighbors.append((exact_x, exact_y + 1))
        else: # straight ahead is down
            if straight > self.distance_threshold:
                neighbors.append((exact_x, exact_y - 1))
            if left > self.distance_threshold:
                neighbors.append((exact_x + 1, exact_y))
            if right > self.distance_threshold:
                neighbors.append((exact_x - 1, exact_y))

        for bor in neighbors:
            self.graph[determined_current].add(bor)
            self.graph[bor].add(determined_current)
            if bor not in self.already_visited:
                self.already_visited.add(bor)
                self.stack.append(bor)
        return


    def get_next_cell(self, x, y, real_coords, heading):
        if not self.next_cell: # assume idealized start
            self.add_current_cell((x, y), real_coords, heading)
            self.next_cell = self.stack.pop()
        desired_x, desired_y = self.next_cell
        if abs(desired_x - x) > self.acceptable_offset or abs(desired_y - y) > self.acceptable_offset:
            return self.next_cell
        if self.state == 2 and desired_x == self.goal[0] and desired_y == self.goal[1]:
            raise Exception('We done here')
        self.add_current_cell(self.next_cell, real_coords, heading)
        if len(self.stack) == 0:
            print('Stack\'s empty, state is {}'.format(self.state))
            if self.state == 0:
                self.stack.append(self.starting_location)
                self.state = 1
            elif self.state == 1:
                self.stack.append(self.goal)
                self.callback()
                self.state = 2
            else:
                raise Exception('We had an empty stack but hadn\'t finished yet. x={}, y={}, graph=\n\n{}'.format(x, y, self.graph))
        p = self.find_shortest_path(self.next_cell, self.stack[-1])
        if not p:
            raise Exception(self.next_cell, self.stack[-1], self.graph)
        p = p[::-1]
        self.stack.extend(p[1:-1])
        self.next_cell = self.stack.pop()
        return self.next_cell


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

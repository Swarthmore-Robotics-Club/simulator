from collections import defaultdict
import math

class DFS():
    def __init__(self, acceptable_offset=0.1, starting_loc=(0.5, 0.5)):
        self.acceptable_offset = acceptable_offset
        self.distance_threshold = 1
        self.already_visited = set([starting_loc])
        self.graph = defaultdict(set)
        self.stack = []
        self.next_cell = None
        self.graph_finished = False
        return


    def _check_current_cell_neighbors(self, current_position, sensor_readings):
        x, y, heading = current_position
        straight, left, right = sensor_readings
        ideal_x = math.floor(x) + .5
        ideal_y = math.floor(y) + .5
        neighbors = []
        if heading < math.pi / 4 or heading > 1.75 * math.pi: # straight ahead is right
            if straight > self.distance_threshold:
                neighbors.append((ideal_x + 1, ideal_y))
            if left > self.distance_threshold:
                neighbors.append((ideal_x, ideal_y + 1))
            if right > self.distance_threshold:
                neighbors.append((ideal_x, ideal_y - 1))
        elif heading < .75 * math.pi: # straight ahead is up
            if straight > self.distance_threshold:
                neighbors.append((ideal_x, ideal_y + 1))
            if left > self.distance_threshold:
                neighbors.append((ideal_x - 1, ideal_y))
            if right > self.distance_threshold:
                neighbors.append((ideal_x + 1, ideal_y))
        elif heading < 1.25 * math.pi: # straight ahead is left
            if straight > self.distance_threshold:
                neighbors.append((ideal_x - 1, ideal_y))
            if left > self.distance_threshold:
                neighbors.append((ideal_x, ideal_y - 1))
            if right > self.distance_threshold:
                neighbors.append((ideal_x, ideal_y + 1))
        else: # straight ahead is down
            if straight > self.distance_threshold:
                neighbors.append((ideal_x, ideal_y - 1))
            if left > self.distance_threshold:
                neighbors.append((ideal_x + 1, ideal_y))
            if right > self.distance_threshold:
                neighbors.append((ideal_x - 1, ideal_y))
        determined_current = (ideal_x, ideal_y)
        for bor in neighbors:
            self.graph[determined_current].add(bor)
            self.graph[bor].add(determined_current)
            if bor not in self.already_visited:
                self.already_visited.add(bor)
                self.stack.append(bor)
        return


    def get_next_cell(self, current_position, sensor_readings):
        if self.graph_finished:
            return None
        if not self.next_cell:
            self._check_current_cell_neighbors(current_position, sensor_readings)
            self.next_cell = self.stack.pop()
        desired_x, desired_y = self.next_cell
        x, y, heading = current_position
        if abs(desired_x - x) > self.acceptable_offset or abs(desired_y - y) > self.acceptable_offset:
            return self.next_cell
        self._check_current_cell_neighbors(current_position, sensor_readings)
        if len(self.stack) == 0:
            self.graph_finished = True
            return None
        p = self.find_shortest_path(self.next_cell, self.stack[-1])
        if not p:
            raise Exception(self.next_cell, self.stack, self.graph)
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

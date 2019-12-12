import enum
import math
import random
from mazes.Labyrinth import Labyrinth
from mazes.MazeGenerator import MazeGenerator
from utils.DFS import DFS
from utils.model import get_individual_proportions
from utils.PIDLoop import PIDLoop
from utils.Position import Position
from Robot import Robot

LENGTH_OF_MAZE = 16
STARTING_LOCATION = (0.5, 0.5, 0.0) # x, y, heading

random.seed(0)

class MicroRobotState(enum.Enum):
    UNKNOWN = 0
    TURNING = 1
    FORWARD = 2


class MacroRobotState(enum.Enum):
    MAPPING = 100
    RETURNING_TO_START = 101
    RACING = 102


def tp(t, n = 4):
    return tuple(map(lambda x: round(x, n), t))

class AMEE(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.wheel_radius = 0.02
        self.encoder_ticks_per_wheel_rev = 225
        self.wheel_base_length = 0.09
        self.max_speed = 0.3
        self._x, self._y, self._heading = STARTING_LOCATION

        # for getting velocities
        self.labyrinth = Labyrinth(MazeGenerator(LENGTH_OF_MAZE, LENGTH_OF_MAZE))
        self.position = Position(*STARTING_LOCATION, self.wheel_radius, self.encoder_ticks_per_wheel_rev)
        self.micro_state = MicroRobotState.UNKNOWN
        self.macro_state = MacroRobotState.MAPPING
        self.clew = DFS()
        self.previous_ticks = (0, 0)
        self.angle_ticker = 0
        self.angle_pid = PIDLoop(5, 0, 0.1)
        self.power_val = 2
        self.acceptable_angle_error = .1
        self.acceptable_physical_offset = 0.01
        self.angle_ticks_needed = 100
        self.next_cell = tuple()

        # for printing the graph
        self.real_xs = []
        self.determined_xs = []
        self.real_ys = []
        self.determined_ys = []
        self.race_start = 0
        return


    def loop(self, dt):
        real_x = self.get_x()
        real_y = self.get_y()
        real_heading = self.get_heading()

        ticks = self.read_encoders()
        sensor_readings = self.labyrinth.get_sensor_readings(real_x, real_y, real_heading)
        self.position.update(ticks, sensor_readings)

        l_vel, r_vel = self._get_velocities(ticks, sensor_readings, dt)
        # print(round(real_heading - self.position.heading, 6), round(real_x - self.position.x, 6), round(real_y - self.position.y, 6), flush=True)

        self.set_left_motor(l_vel)
        self.set_right_motor(r_vel)
        self.determined_xs.append(self.position.x)
        self.real_xs.append(real_x)
        self.determined_ys.append(self.position.y)
        self.real_ys.append(real_y)
        return
    

    def _get_velocities(self, ticks, sensor_readings, dt):
        x, y = self.position.x, self.position.y
        if self.micro_state == MicroRobotState.UNKNOWN:
            idealized_coords = math.floor(x) + .5, math.floor(y) + .5

            if self.macro_state == MacroRobotState.MAPPING:
                self.next_cell = self.clew.get_next_cell(self.position.as_tuple(), sensor_readings)
                if self.next_cell == None: # we finished mapping the maze, DFS is done
                    self.macro_state = MacroRobotState.RETURNING_TO_START

            if self.macro_state == MacroRobotState.RETURNING_TO_START:
                if idealized_coords == STARTING_LOCATION[:2]: # we're back to the start
                    self.race_start = len(self.real_xs)
                    self.macro_state = MacroRobotState.RACING
                else:
                    p = self.clew.find_shortest_path(idealized_coords, STARTING_LOCATION[:2])
                    if p == None:
                        raise Exception(idealized_coords, self.clew.graph, self.position.as_tuple())
                    self.next_cell = p[1] # first item is current cell

            if self.macro_state == MacroRobotState.RACING:
                p = self.clew.find_shortest_path(idealized_coords, self.labyrinth.goal)
                if p == None:
                    raise Exception('We finished.')
                self.next_cell = p[1] # first item is current cell
            self.micro_state = MicroRobotState.TURNING
        angle_error = self._get_angle_error(*self.position.as_tuple())
        angular_vel = self.angle_pid.updateErrorPlus(angle_error, dt)

        if self.micro_state == MicroRobotState.TURNING:
            if abs(angle_error) < self.acceptable_angle_error:
                if self.angle_ticker < self.angle_ticks_needed:
                    self.angle_ticker += 1
                else:
                    self.angle_ticker = 0
                    self.micro_state = MicroRobotState.FORWARD
            else:
                self.angle_ticker = 0
            return get_individual_proportions(0, angular_vel, self.wheel_radius, self.wheel_base_length)
            
        if self.micro_state == MicroRobotState.FORWARD:
            if self._should_slow_down(x, y):
                return self._slow_down()
            vel = self.max_speed / (abs(angular_vel) + 1)**self.power_val
            return get_individual_proportions(vel, angular_vel, self.wheel_radius, self.wheel_base_length)
        raise Exception('Micro state: {}, macro state: {}, position: {}'.format(self.micro_state, self.macro_state, self.position.as_tuple()))


    def _get_angle_error(self, x, y, heading):
        desired_angle = math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)
        diff = desired_angle - heading
        return math.atan2(math.sin(diff), math.cos(diff))


    def _should_slow_down(self, x, y):
        return abs(self.next_cell[0] - x) < self.acceptable_physical_offset and abs(self.next_cell[1] - y) < self.acceptable_physical_offset


    def _slow_down(self):
        self.micro_state = MicroRobotState.UNKNOWN
        return (0, 0)


    def print_graphs(self):
        self.labyrinth.draw_lines(self.real_xs[:self.race_start], self.real_ys[:self.race_start], 'lightblue')
        self.labyrinth.draw_lines(self.real_xs[self.race_start:], self.real_ys[self.race_start:], 'midnightblue')
        self.labyrinth.draw_lines(self.determined_xs[:self.race_start], self.determined_ys[:self.race_start], 'salmon')
        self.labyrinth.draw_lines(self.determined_xs[self.race_start:], self.determined_ys[self.race_start:], 'red')
        self.labyrinth.display()
        return

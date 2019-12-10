import enum
import math
import random
from mazes.Labyrinth import Labyrinth
from mazes.MazeGenerator import MazeGenerator
from utils.DFS import DFS
from utils.model import get_individual_proportions
from utils.PIDLoop import PIDLoop
from Robot import Robot

LENGTH_OF_MAZE = 16
STARTING_LOCATION = (0.5, 0.5, 0.0) # x, y, heading

random.seed(0)

class RobotState(Enum):
    UNKNOWN = 0
    TURNING = 1
    FORWARD = 2

class AMEE(Robot):
    def __init__(self):
        Robot.__init__(self)
        self.wheel_radius = 0.02
        self.encoder_ticks_per_wheel_rev = 225
        self.wheel_base_length = 0.09
        self.max_vel = 0.3

        # for getting velocities
        self.labyrinth = Labyrinth(MazeGenerator(LENGTH_OF_MAZE, LENGTH_OF_MAZE).maze)
        self.position = (*STARTING_LOCATION)
        self.state = RobotState.UNKNOWN
        self.dfs = DFS()
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


    def _set_race_start(self):
        self.race_start = len(self.real_xs)
        return


    def loop(self, dt):
        real_x = self.get_x()
        real_y = self.get_y()
        real_heading = self.get_heading()

        ticks = self.read_encoders()
        sensors = self.labyrinth.get_sensor_readings(real_x, real_y, real_heading)

        l_vel, r_vel = self._get_velocities(ticks, sensors, dt)
        self._update_position(ticks)

        self.set_left_motor(l_vel)
        self.set_right_motor(r_vel)
        self.determined_xs.append(self.position[0])
        self.real_xs.append(real_x)
        self.determined_ys.append(self.position[1])
        self.real_ys.append(real_y)
        return


    def _update_position(self, ticks):
        ticks_left, ticks_right = ticks
        diff_ticks_left = ticks_left - self.previous_ticks[0]
        diff_ticks_right = ticks_right - self.previous_ticks[1]
        self.previous_ticks = (ticks_left, ticks_right)

        d_left_wheel = TWO_PI * self.wheel_radius * (diff_ticks_left / self.encoder_ticks_per_wheel_rev)
        d_right_wheel = TWO_PI * self.wheel_radius * (diff_ticks_right / self.encoder_ticks_per_wheel_rev)
        d_center = (d_left_wheel + d_right_wheel) / 2

        prev_x, prev_y, prev_heading = self.position
        new_x = prev_x + (d_center * math.cos(prev_heading))
        new_y = prev_y + (d_center * math.sin(prev_heading))
        new_heading = math.fmod(prev_heading + ((d_right_wheel - d_left_wheel) / 2) + TWO_PI, TWO_PI)
        self.position = (new_x, new_y, new_heading)
        return
    

    def _get_velocities(self, ticks, sensors, dt):
        x, y = self.position[:2]
        angle_error = self._get_angle_error(*self.position)
        angular_vel = self.angle_pid.updateErrorPlus(angle_error, dt)
        if self.state == RobotState.UNKNOWN:
            self.next_cell = self.dfs.get_next_cell()
            if angle_error < self.acceptable_angle_error:
                self.state = RobotState.FORWARD
            else:
                self.state = RobotState.TURNING
        if self.state == RobotState.TURNING:
            if abs(angle_error) < self.acceptable_angle_error:
                if self.angle_ticker < self.angle_ticks_needed:
                    self.angle_ticker += 1
                else:
                    self.angle_ticker = 0
                    self.state = RobotState.FORWARD
            else:
                self.angle_ticker = 0
        if self.state == RobotState.FORWARD:
            if self._should_slow_down(x, y):
                return self._slow_down()
            vel = self.max_vel / (abs(angular_vel) + 1)**self.power_val
            return get_individual_proportions(vel, angular_vel)
        raise Exception('State: {}, position: {}'.format(self.state, self.position))


    def _get_angle_error(self, x, y, heading):
        desired_angle = math.atan2(self.next_cell[1] - y, self.next_cell[0] - x)
        diff = desired_angle - heading
        return math.atan2(math.sin(diff), math.cos(diff))


    def _should_slow_down(self, x, y):
        return abs(self.next_cell[0] - x) < self.acceptable_physical_offset and abs(self.next_cell[1] - y) < self.acceptable_physical_offset


    def _slow_down(self):
        self.state = RobotState.UNKNOWN
        return (0, 0)


    def print_graphs(self):
        self.labyrinth.draw_lines(self.real_xs[:self.race_start], self.real_ys[:self.race_start], 'lightblue')
        self.labyrinth.draw_lines(self.real_xs[self.race_start:], self.real_ys[self.race_start:], 'midnightblue')
        self.labyrinth.draw_lines(self.determined_xs[:self.race_start], self.determined_ys[:self.race_start], 'salmon')
        self.labyrinth.draw_lines(self.determined_xs[self.race_start:], self.determined_ys[self.race_start:], 'red')
        self.labyrinth.display()
        return

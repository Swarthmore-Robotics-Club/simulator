import pygame 
from MazeGenerator import MazeCell, MazeGenerator
import json
from random import seed

pygame.init()

def json_to_maze(path):
    cell_arr = []
    with open(path) as f:
        data = json.load(f)
        for cell in data['cells']:
            new_cell = MazeCell(cell['x'], cell['y'])
            new_cell.walls = cell['walls']
            cell_arr.append(new_cell)
    return cell_arr


def draw_maze_cell(maze_cell, screen, width):
    x = maze_cell.x * width
    y = maze_cell.y * width
    stroke = (0, 0, 0)
    if maze_cell.walls[0]:
        start = (x, y)
        end = (x + width, y)
        pygame.draw.line(screen, stroke, start, end) 
    if maze_cell.walls[1]:
        start = (x + width, y)
        end = (x + width, y + width)
        pygame.draw.line(screen, stroke, start, end)
    if maze_cell.walls[2]:
        start = (x + width, y + width)
        end = (x , y + width)
        pygame.draw.line(screen, stroke, start, end)
    if maze_cell.walls[3]:
        start = (x, y + width)
        end = (x , y)
        pygame.draw.line(screen, stroke, start, end)
    return


def display(maze, width, height, cell_width): 
    screen = pygame.display.set_mode((width, height))
    cols = width // cell_width
    rows = height // cell_width
    screen.fill((255,255,255))
    for row in maze:
        for cell in row:
            draw_maze_cell(cell, screen, cell_width)
    pygame.display.flip()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
    return


def _display_test():
    seed(0)
    width = 800
    height = 800
    cell_width = 50
    cols = width // cell_width
    rows = height // cell_width
    gen = MazeGenerator(rows, cols)
    display(gen.maze, width, height, cell_width)
    return

if __name__ == '__main__':
    _display_test()

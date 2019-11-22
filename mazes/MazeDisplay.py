import pygame 
from MazeGenerator import MazeCell, MazeGenerator
import json
from random import seed

pygame.init()

def json_to_maze(path):
    with open(path) as file:
        data = json.load(file)
        cell_arr = []
        for cell in data['cells']:
            x = cell['x']
            y = cell['y']
            walls = cell['walls']

            new_cell = MazeCell(x, y)
            new_cell.walls = walls
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


def display_from_json(path):
    #TODO remove hard coded screen size and cell width
    width = 800
    height = 800
    cell_width = 160
    cols = width // cell_width
    rows = height // cell_width
    running = 1
    maze = json_to_maze(path)
    screen = pygame.display.set_mode((width, height))


    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0 
        screen.fill((255,255,255))

        for cell in maze:
            draw_maze_cell(cell, screen, cell_width)

        pygame.display.flip()



def display(maze, width, height, cell_width): 
    
    screen = pygame.display.set_mode((width, height))
    
    cols = width // cell_width
    rows = height // cell_width
    running = 1
    

    while running:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0 
        screen.fill((255,255,255))

        for row in maze:
            for cell in row:
                draw_maze_cell(cell, screen, cell_width)
        pygame.display.flip()

def _display_test():
    seed(0)
    width = 800
    height = 800
    cell_width = 160
    cols = width // cell_width
    rows = height // cell_width
    gen = MazeGenerator(rows, cols)
    maze = gen.maze

    display(maze, width, height, cell_width)

def _disply_test_json():
    pass


_display_test()
# display_from_json('mazes/sample_maze.json')

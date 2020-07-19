import pygame
import math
from queue import PriorityQueue

# Window set up
WIDTH = 800
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
TURQUOISE = (64, 224, 208)
GREY = (128, 128, 128)


# Class for creating and handling each cube that is being changed
class Cube:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def getpos(self):
        return self.row, self.col

    def scanned(self):
        return self.color == RED

    def not_scanned(self):
        return self.color == ORANGE

    def blocked(self):
        return self.color == BLACK

    def start_point(self):
        return self.color == GREEN

    def end_point(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def draw_scanned(self):
        self.color = RED

    def draw_unscanned(self):
        self.color = ORANGE

    def draw_blocked(self):
        self.color = BLACK

    def draw_end(self):
        self.color = PURPLE

    def draw_start(self):
        self.color = GREEN

    def draw_path(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].blocked():  # Down a block
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].blocked():  # Up a block
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].blocked():  # Left a block
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].blocked():  # Right a block
            self.neighbors.append(grid[self.row][self.col + 1])

    # Less than
    def __lt__(self, other):
        return False


# Heuristic or distance used for finding closest path. In this case I have chosen euclidean distance
def manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Function for making the grid
def set_grid(rows, width):
    grid = []
    space = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cube = Cube(i, j, space, rows)
            grid[i].append(cube)

    return grid


# Function for drawing the grid
def draw_grid(win, rows, width):
    space = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * space), (width, i * space))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * space, 0), (j * space, width))


# Function to find the position of the mouse click
def clicked_pos(pos, rows, width):
    space = width // rows
    y, x = pos

    row = y // space
    col = x // space
    return row, col


def build_path(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.draw_path()
        draw()


def astar(draw, grid, start, end):
    count = 0
    open_list = PriorityQueue()
    open_list.put((0, count, start))
    parent = {}
    g = {cube: float("inf") for row in grid for cube in row}
    g[start] = 0
    f = {cube: float("inf") for row in grid for cube in row}
    f[start] = manhattan(start.getpos(), end.getpos())

    open_list_hash = {start}

    while not open_list.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_list.get()[2]
        open_list_hash.remove(current)

        if current == end:
            build_path(parent, end, draw)
            end.draw_end()
            return True

        for neighbor in current.neighbors:
            temp_g = g[current] + 1
            if temp_g < g[neighbor]:
                parent[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + manhattan(neighbor.getpos(), end.getpos())
                if neighbor not in open_list_hash:
                    count += 1
                    open_list.put((f[neighbor], count, neighbor))
                    open_list_hash.add(neighbor)
                    neighbor.draw_unscanned()
        draw()

        if current != start:
            current.draw_scanned()
    return False


# Draw the window
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for cube in row:
            cube.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


# Main loop for the visualizer
def main(win, width):
    ROWS = 50
    grid = set_grid(ROWS, width)

    start = None
    end = None

    run = True
    # Loop to keep the pygame window running until exit
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = clicked_pos(pos, ROWS, width)
                cube = grid[row][col]
                if not start and cube != end:
                    start = cube
                    start.draw_start()
                elif not end and cube != start:
                    end = cube
                    end.draw_end()
                elif cube != end and cube != start:
                    cube.draw_blocked()

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = clicked_pos(pos, ROWS, width)
                cube = grid[row][col]
                cube.reset()
                if cube == start:
                    start = None
                elif cube == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cube in row:
                            cube.update_neighbors(grid)

                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

    pygame.quit()


main(WIN, WIDTH)

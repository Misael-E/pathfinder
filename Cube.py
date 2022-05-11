import pygame

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

    def blocked(self):
        return self.color == BLACK

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
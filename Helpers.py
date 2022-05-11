from Cube import *

# Function to build path once algorithm finds one
def build_path(parent, current, draw):
    while current in parent:
        current = parent[current]
        current.draw_path()
        draw()

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

# Draw the window
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for cube in row:
            cube.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()
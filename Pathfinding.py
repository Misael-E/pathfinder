import pygame
from tkinter import *
from tkinter import messagebox

from Cube import *
from Helpers import *
from Algorithms import dijkstra, astar

# Window set up
WIDTH = 800
HEIGHT = 800

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualizer")

# Main loop for the visualizer
def main(win, width):
    ROWS = 50
    grid = set_grid(ROWS, width)

    start = None
    end = None

    run = True

    Tk().wm_withdraw()
    messagebox.showinfo("Instructions", "1. Simply pick two points for your start (Green) and end (Purple).\n"
                                        "\n2. Then draw your barriers or obstacles (Black).\n"
                                        "\n3. Then on your keyboard, press one for A*Algorithm or two for Dijkstras "
                                        "Algorithm.\n"
                                        "\n4. To clear the grid press r.")

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
                if event.key == pygame.K_1 and start and end:
                    for row in grid:
                        for cube in row:
                            cube.update_neighbors(grid)

                    # AStar pathfinding algorithm
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_2 and start and end:
                    for row in grid:
                        for cube in row:
                            cube.update_neighbors(grid)

                    # Dijkstra's pathfinding algorithm
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = set_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)

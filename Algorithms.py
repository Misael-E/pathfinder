import pygame
from queue import PriorityQueue
from Cube import *
from Helpers import *

def dijkstra(draw, grid, start, end):
    count = 0
    open_list = PriorityQueue()
    open_list.put((0, count, start))
    parent = {}
    g = {cube: float("inf") for row in grid for cube in row}
    g[start] = 0

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
                if neighbor not in open_list_hash:
                    count += 1
                    open_list.put((g[neighbor], count, neighbor))
                    open_list_hash.add(neighbor)
                    neighbor.draw_unscanned()
        draw()

        if current != start:
            current.draw_scanned()
    return False


def astar(draw, grid, start, end):
    count = 0
    open_list = PriorityQueue()
    open_list.put((0, count, start))
    parent = {}
    g = {cube: float("inf") for row in grid for cube in row}
    g[start] = 0
    h = {cube: float("inf") for row in grid for cube in row}
    h[start] = manhattan(start.getpos(), end.getpos())

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
                h[neighbor] = temp_g + manhattan(neighbor.getpos(), end.getpos())
                if neighbor not in open_list_hash:
                    count += 1
                    open_list.put((h[neighbor], count, neighbor))
                    open_list_hash.add(neighbor)
                    neighbor.draw_unscanned()
        draw()

        if current != start:
            current.draw_scanned()
    return False
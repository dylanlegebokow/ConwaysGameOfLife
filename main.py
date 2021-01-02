import numpy as np
import pygame
import sys
import random

from patterns import *

# Matrix variables
width = 150
height = 80
cell_size = 6

# Color Palette
color_alive_1 = (31, 171, 137)
color_alive_2 = (98, 210, 162)
color_alive_3 = (157, 243, 196)
color_alive = [color_alive_1, color_alive_2, color_alive_3]
color_grid = (20, 20, 20)
color_background = (10, 10, 10)


# Creates an numpy 2d array for the next generation
def next_generation(matrix):

    # Create matrix to be returned
    matrix_updated = np.zeros((width, height))

    # Iterate through entire grid
    for w in range(0, width):
        for h in range(0, height):

            # Find adjacency matrix for each cell
            if w == 0 and h != 0:
                temp = matrix[w:w + 2, h - 1:h + 2]
            elif w != 0 and h == 0:
                temp = matrix[w - 1:w + 2, h:h + 2]
            elif w == 0 and h == 0:
                temp = matrix[w:w + 2, h:h + 2]
            else:
                temp = matrix[w - 1:w + 2, h - 1:h + 2]

            # Determine the number of neighbors a cell has
            neighbors = np.sum(temp) - matrix[w, h]

            # Determine if the cell will live or die
            if matrix[w, h] == 1 and (neighbors == 2 or neighbors == 3):
                matrix_updated[w, h] = 1
            elif matrix[w, h] == 0 and neighbors == 3:
                matrix_updated[w, h] = 1
            else:
                matrix_updated[w, h] = 0

    return matrix_updated


# Sets the color of a cell depending on if it is alive (1) or dead (0)
def get_color(matrix, surface):

    # Iterate through entire grid
    for w in range(0, width):
        for h in range(0, height):
            if matrix[w, h] == 1:
                color = random.choice(color_alive)
            else:
                color = color_background
            pygame.draw.rect(surface, color, (w*cell_size, h*cell_size, cell_size-2, cell_size-2))


def main():

    cmd_input = ''
    try:
        cmd_input = str(sys.argv[1])
    except:
        print("\nError: Missing parameter")
    if cmd_input == '0':
        # Initial random array
        matrix = np.random.choice(2, (width, height))
    elif cmd_input == '1':
        # Enables running the test patterns
        matrix = np.zeros((width, height))
        for i in test_patterns:
            matrix[i[0], i[1]] = 1
    else:
        print("\nPlease execute the code with the following parameter:")
        print("  0 : Random initial array")
        print("  1 : Run testing array\n")
        print("For example:\n  $ python main.py 0")
        exit()

    # Setup and run the dialog
    pygame.init()
    surface = pygame.display.set_mode((width * cell_size, height * cell_size))
    pygame.display.set_caption("Conway's Game of Life")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        surface.fill(color_grid)
        get_color(matrix, surface)
        matrix = next_generation(matrix)
        pygame.display.update()


if __name__ == "__main__":
    main()

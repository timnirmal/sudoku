import random

import numpy as np
from matplotlib import pyplot as plt


def is_valid(grid, row, col, num):
    # Check if the number is not repeated in the row, column and 3x3 subgrid
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True


def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


def generate_sudoku(num_holes):
    # Initialize empty grid
    grid = [[0 for _ in range(9)] for _ in range(9)]

    # Fill the diagonal 3x3 grids
    for i in range(0, 9, 3):
        num_list = random.sample(range(1, 10), 9)
        for row in range(3):
            for col in range(3):
                grid[i + row][i + col] = num_list.pop()

    # Fill remaining cells
    solve_sudoku(grid)

    # Remove numbers to create holes
    for _ in range(num_holes):
        x, y = random.randint(0, 8), random.randint(0, 8)
        while grid[x][y] == 0:
            x, y = random.randint(0, 8), random.randint(0, 8)
        grid[x][y] = 0

    return grid


def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else "." for num in row))


def generate_sudoku_image(grid):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(np.arange(0, 10, 1))
    ax.set_yticks(np.arange(0, 10, 1))
    ax.grid(which='both', color='black', linewidth=2)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    for i in range(9):
        for j in range(9):
            num = grid[i][j]
            if num != 0:
                ax.text(j + 0.5, 8.5 - i, str(num), va='center', ha='center', fontsize=14)

    # Adding thicker lines for Sudoku blocks
    for i in range(0, 10, 3):
        ax.axhline(y=i, color='black', linewidth=4)
        ax.axvline(x=i, color='black', linewidth=4)

    # dont show the axes
    plt.axis('off')

    # add 9 horizontal and vertical lines
    for i in range(0, 9):
        plt.axhline(i, lw=2, color='black')
        plt.axvline(i, lw=2, color='black')

    plt.gca().invert_yaxis()
    # save image
    plt.savefig('sudoku 9x9.png')
    plt.show()


# Generate and print a Sudoku puzzle
puzzle = generate_sudoku(40)  # Adjust the number of holes for difficulty
print_grid(puzzle)
generate_sudoku_image(puzzle)

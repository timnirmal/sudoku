import random
import numpy as np
from matplotlib import pyplot as plt


def is_valid_16x16(grid, row, col, num):
    # Check if the number is not repeated in the row, column and 4x4 subgrid
    for x in range(16):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 4 * (row // 4), 4 * (col // 4)
    for i in range(start_row, start_row + 4):
        for j in range(start_col, start_col + 4):
            if grid[i][j] == num:
                return False
    return True


def solve_sudoku_16x16(grid):
    for row in range(16):
        for col in range(16):
            if grid[row][col] == 0:
                for num in range(1, 17):
                    if is_valid_16x16(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku_16x16(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True


def generate_sudoku_16x16(num_holes):
    # Initialize empty grid
    grid = [[0 for _ in range(16)] for _ in range(16)]

    # Fill the grid
    solve_sudoku_16x16(grid)

    # Remove numbers to create holes
    for _ in range(num_holes):
        x, y = random.randint(0, 15), random.randint(0, 15)
        while grid[x][y] == 0:
            x, y = random.randint(0, 15), random.randint(0, 15)
        grid[x][y] = 0

    return grid


def generate_sudoku_image_16x16(grid):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 16)
    ax.set_xticks(np.arange(0, 17, 1))
    ax.set_yticks(np.arange(0, 17, 1))
    ax.grid(which='both', color='black', linewidth=4)
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    for i in range(16):
        for j in range(16):
            num = grid[i][j]
            if num != 0:
                ax.text(j + 0.5, 15.5 - i, str(num), va='center', ha='center', fontsize=10)

    # Adding thicker lines for Sudoku blocks
    for i in range(0, 17, 4):
        ax.axhline(y=i, color='black', linewidth=4)
        ax.axvline(x=i, color='black', linewidth=4)

    # dont show the axes
    plt.axis('off')

    # add 16 horizontal and vertical lines
    for i in range(0, 17):
        plt.axhline(i, lw=2, color='black')
        plt.axvline(i, lw=2, color='black')

    # Invert the y-axis to display the puzzle in the right order
    plt.gca().invert_yaxis()
    # save image
    plt.savefig('sudoku 16x16.png')
    plt.show()


# Generate a 16x16 Sudoku puzzle
puzzle_16x16 = generate_sudoku_16x16(2)  # Adjust the number of holes for difficulty
generate_sudoku_image_16x16(puzzle_16x16)

import time

input_path = "../Sudoku Sample Puzzles/Sample Inputs/input1.txt"

# Initialize an empty 2D array for the Sudoku puzzle
sudoku_puzzle = []

# Read the text file and convert it into a 2D array
with open(input_path, 'r') as f:
    for line in f:
        # Split each line into individual values and convert them to integers
        row = [int(x) for x in line.strip().split()]
        sudoku_puzzle.append(row)

# # Print the 2D array
# for row in sudoku_puzzle:
#     print(row)

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)

    if not empty_cell:
        return True

    row, col = empty_cell
    remaining_values = get_remaining_values(board, row, col)

    # Sort the remaining values by the least constraining value heuristic
    sorted_values = sorted(remaining_values, key=lambda x: count_constrained_cells(board, row, col, x))

    for num in sorted_values:
        if is_valid_move(board, num, (row, col)):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False


def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def get_remaining_values(board, row, col):
    used_values = set(board[row]) | set(board[i][col] for i in range(9)) | set(get_box_values(board, row, col))
    return [num for num in range(1, 10) if num not in used_values]


def get_box_values(board, row, col):
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    return [board[i][j] for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)]


def count_constrained_cells(board, row, col, num):
    count = 0
    for i in range(9):
        if board[row][i] == 0 and num in get_remaining_values(board, row, i):
            count += 1
        if board[i][col] == 0 and num in get_remaining_values(board, i, col):
            count += 1
    return count




def is_valid_move(board, num, pos):
    row, col = pos
    # Check row
    if num in board[row]:
        return False

    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True


if __name__ == '__main__':
    start_time = time.time()
    # Call the solve_sudoku function to solve the puzzle
    if solve_sudoku(sudoku_puzzle):
        # Print the solved Sudoku puzzle
        for row in sudoku_puzzle:
            print(row)
    else:
        print("No solution exists for the given Sudoku puzzle.")

    print("--- %s seconds ---" % (time.time() - start_time))


from time import time

from colorama import Fore, Style, init, Back

from solver.validator import sudoku_validator

init()

number_of_attempts = 0


class EmptySpace:
    def __init__(self, row_index, col_index):
        self.row = row_index
        self.col = col_index
        self.subMatrix = find_submatrix_no(row_index, col_index)
        self.value = '0'
        self.potentialVals = set()

    def set_potential_vals(self, potential_vals):
        self.potentialVals = potential_vals

    def set_value(self, value):
        self.value = value

    def __lt__(self, other):
        return len(self.potentialVals) < len(other.potentialVals)


def increase_attempt_count():
    global number_of_attempts
    number_of_attempts += 1


def load_and_prepare_puzzle(filepath):
    sudoku_puzzle = []
    available_vals = set()

    with open(filepath, 'r') as file:
        for line in file:
            line_values = line.strip().split()
            sudoku_puzzle.append(line_values)

            # Find available values (non-zero) and add them to the set
            for val in line_values:
                if val != '0':
                    available_vals.add(val)

    return sudoku_puzzle, available_vals


def create_value_sets(puzzle):
    size = len(puzzle)  # Assuming puzzle is always a square matrix
    submatrix_size = int(size ** 0.5)

    row_val_sets = [set() for _ in range(size)]
    col_val_sets = [set() for _ in range(size)]
    sub_matrix_sets = [set() for _ in range(size)]

    for row in range(size):
        for col in range(size):
            val = puzzle[row][col]
            if val != '0':
                # Add value to row and column sets
                row_val_sets[row].add(val)
                col_val_sets[col].add(val)

                # Calculate sub-matrix index and add value
                sub_matrix_no = (row // submatrix_size) * submatrix_size + col // submatrix_size
                sub_matrix_sets[sub_matrix_no].add(val)

    return row_val_sets, col_val_sets, sub_matrix_sets


def find_submatrix_no(row, col):
    return (row // 4) * 4 + col // 4


def create_empty_cells(puzzle):
    empty_cells = []
    for row in range(len(puzzle)):
        for col in range(len(puzzle[0])):
            if puzzle[row][col] == '0':
                empty_cells.append(EmptySpace(row, col))
    return empty_cells


def print_sudoku(puzzle_matrix):
    # Define colors for highlighting
    highlighted_row = Fore.YELLOW
    highlighted_col = Fore.GREEN
    highlighted_zero = Fore.RED
    green = Fore.GREEN + Back.RESET + Style.BRIGHT
    reset_style = Style.RESET_ALL

    for row_index, row in enumerate(puzzle_matrix):
        if row_index % 4 == 0 and row_index != 0:
            print('-' * 37)

        for colIndex, val in enumerate(row):
            if colIndex % 4 == 0 and colIndex != 0:
                print('|', end=' ')

            if row_index % 4 == 0 or colIndex % 4 == 0:
                # Highlight boxes (borders) in yellow
                if val == '0':
                    print(highlighted_row + highlighted_col + highlighted_zero + val + reset_style, end=' ')
                else:
                    print(highlighted_row + highlighted_col + val + reset_style, end=' ')
            else:
                # Highlight other symbols (grid lines and non-'0' values) in green
                if val == '0':
                    print(highlighted_zero + val + reset_style, end=' ')
                else:
                    print(green + val + reset_style, end=' ')

            if colIndex == len(row) - 1:
                print()


def puzzle_is_solved(empty_cells, row_val_sets, col_val_sets, sub_matrix_sets, available_vals):
    if all_cells_have_potential_vals(empty_cells, row_val_sets, col_val_sets, sub_matrix_sets, available_vals):
        empty_cell = empty_cells.pop(0)
        for potentialVal in empty_cell.potentialVals:
            empty_cell.set_value(potentialVal)
            increase_attempt_count()
            add_to_available_vals_sets(empty_cell, row_val_sets, col_val_sets, sub_matrix_sets)
            if is_puzzle_solved(row_val_sets, col_val_sets, sub_matrix_sets):
                empty_cells.insert(0, empty_cell)
                return True
            else:
                if puzzle_is_solved(empty_cells, row_val_sets, col_val_sets, sub_matrix_sets, available_vals):
                    empty_cells.insert(0, empty_cell)
                    return True
                remove_from_available_vals_sets(empty_cell, row_val_sets, col_val_sets, sub_matrix_sets)
            empty_cell.set_value('0')
        empty_cells.insert(0, empty_cell)
        return False
    else:
        return False


def all_cells_have_potential_vals(empty_cells, row_val_sets, col_val_sets, sub_matrix_sets, available_vals):
    for emptyCell in empty_cells:
        existing_vals_in_row_col_sub_matrix = row_val_sets[emptyCell.row] | col_val_sets[emptyCell.col] | \
                                              sub_matrix_sets[
                                                  emptyCell.subMatrix]
        potential_vals = available_vals - existing_vals_in_row_col_sub_matrix
        if potential_vals:
            emptyCell.set_potential_vals(potential_vals)
        else:
            return False
    empty_cells.sort()
    return True


def add_to_available_vals_sets(empty_cell, row_val_sets, col_val_sets, sub_matrix_sets):
    row_val_sets[empty_cell.row].add(empty_cell.value)
    col_val_sets[empty_cell.col].add(empty_cell.value)
    sub_matrix_sets[empty_cell.subMatrix].add(empty_cell.value)


def is_puzzle_solved(row_val_sets, col_val_sets, sub_matrix_sets):
    puzzle_length = 16
    for rowValSet in row_val_sets:
        if len(rowValSet) != puzzle_length:
            return False
    for colValSet in col_val_sets:
        if len(colValSet) != puzzle_length:
            return False
    for subMatrixValSet in sub_matrix_sets:
        if len(subMatrixValSet) != puzzle_length:
            return False
    return True


def remove_from_available_vals_sets(empty_cell, row_val_sets, col_val_sets, sub_matrix_sets):
    row_val_sets[empty_cell.row].discard(empty_cell.value)
    col_val_sets[empty_cell.col].discard(empty_cell.value)
    sub_matrix_sets[empty_cell.subMatrix].discard(empty_cell.value)


def write_solution_to_file(filepath, puzzle, is_solved):
    print(filepath)  # ../Sudoku Sample Puzzles/Sample Inputs/input_hex1.txt
    # get only the "input_hex1" part
    output_file = f"{filepath.split('/')[-1].split('.')[0]}_output.txt"
    with open(output_file, 'w') as file:
        if is_solved:
            for row in puzzle:
                file.write(' '.join(row) + '\n')
        else:
            file.write('No Solution\n')


def solve_sudoku_16x16(input_data_path):
    puzzle_matrix, available_vals = load_and_prepare_puzzle(input_data_path)
    row_val_sets, col_val_sets, sub_matrix_sets = create_value_sets(puzzle_matrix)
    empty_cells = create_empty_cells(puzzle_matrix)

    # Validation and initial display
    is_valid, is_valid_text = sudoku_validator(puzzle_matrix)
    if not is_valid:
        print('Is the puzzle valid?', is_valid_text)
    print_sudoku(puzzle_matrix)

    # Start solving
    start_time = time()
    is_solved = puzzle_is_solved(empty_cells, row_val_sets, col_val_sets, sub_matrix_sets, available_vals)
    end_time = time()

    # Results
    if is_solved:
        print('Sudoku solved!')
        print(f'Number of attempts: {number_of_attempts}')
        print(f'Time taken to solve: {end_time - start_time:.5f} seconds')
        update_sudoku_with_solution(puzzle_matrix, empty_cells)
        print_sudoku(puzzle_matrix)
        is_valid, is_valid_text = sudoku_validator(puzzle_matrix)
        if not is_valid:
            print('Is the puzzle valid?', is_valid_text)
        write_solution_to_file(input_data_path, puzzle_matrix, is_solved=True)
    else:
        print('No solution!')
        write_solution_to_file(input_data_path, None, is_solved=False)

    return is_solved


def update_sudoku_with_solution(matrix, empty_cells):
    for cell in empty_cells:
        matrix[cell.row][cell.col] = cell.value


# if __name__ == "__main__":
#     input_path = "../Sudoku Sample Puzzles/Sample Inputs/input_hex1.txt"
#     solve_sudoku_16x16(input_path)

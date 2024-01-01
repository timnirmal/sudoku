def is_valid_sudoku_val(puzzle, length, block_size):
    def is_valid_group(group, group_type, index):
        if len(group) != length or any(n <= 0 or n > length for n in group):
            print(f"Invalid values in {group_type} {index}: {group}")
            return False
        if len(set(group)) != length:
            print(f"Duplicate values in {group_type} {index}: {group}")
            return False
        return True

    # Check rows and columns
    for i in range(length):
        row = [puzzle[i * length + j] for j in range(length)]
        col = [puzzle[j * length + i] for j in range(length)]
        if not is_valid_group(row, "row", i) or not is_valid_group(col, "column", i):
            return False

    # Check blocks
    for i in range(0, length, block_size):
        for j in range(0, length, block_size):
            block = [puzzle[x * length + y] for x in range(i, i + block_size) for y in range(j, j + block_size)]
            block_index = (i // block_size, j // block_size)
            if not is_valid_group(block, "block", block_index):
                return False

    return True


# Using the previously defined sudoku_validator function to check the board
def sudoku_validator_int(board):
    # print(check_data_types(board))
    # check data type
    if not isinstance(board, list):
        return False, "Invalid board type: not a list"

    # check data type of each cell
    for row in board:
        if not isinstance(row, list):
            return False, "Invalid board type: not a list of lists"
        for cell in row:
            # print(type(cell))
            if not isinstance(cell, str):
                return False, "Invalid board type: not a list of lists of integers"

    # Check board dimensions
    if len(board) != 16 or any(len(row) != 16 for row in board):
        return False, "Invalid board size"

    # Check for invalid numbers or characters
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if not isinstance(cell, int) or not (1 <= cell <= 16):
                return False, f"Invalid character or number at ({i + 1}, {j + 1})"

    # Function to check if a block is valid
    def is_valid_block(block):
        non_zero_block = [x for x in block if x != 0]
        return len(non_zero_block) == len(set(non_zero_block))

    # Check rows and columns for duplicates
    for i in range(16):
        row = board[i]
        column = [board[j][i] for j in range(16)]
        if not is_valid_block(row):
            return False, f"Duplicate number in row {i + 1}"
        if not is_valid_block(column):
            return False, f"Duplicate number in column {i + 1}"

    # Check 4x4 subgrids for duplicates
    for i in range(0, 16, 4):
        for j in range(0, 16, 4):
            block = [board[x][y] for x in range(i, i + 4) for y in range(j, j + 4)]
            if not is_valid_block(block):
                return False, f"Duplicate number in block starting at ({i + 1}, {j + 1})"

    return True, "Valid and complete Sudoku board"


def sudoku_validator(board):
    # Check board type
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        return False, "Invalid board type: not a list of lists"

    # Check board dimensions
    if len(board) != 16 or any(len(row) != 16 for row in board):
        return False, "Invalid board size"

    # Check for invalid numbers or characters
    incomplete = False
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if not isinstance(cell, str) or not (cell.isdigit() and (1 <= int(cell) <= 16) or cell == '0'):
                return False, f"Invalid character or number at ({i + 1}, {j + 1})"
            if cell == '0':
                incomplete = True

    # Function to check if a block is valid
    def is_valid_block(block):
        block = [x for x in block if x != '0']
        return len(block) == len(set(block))

    # Check rows and columns for duplicates
    for i in range(16):
        row = board[i]
        column = [board[j][i] for j in range(16)]
        if not is_valid_block(row) or not is_valid_block(column):
            return False, "Duplicate number in row or column"

    # Check 4x4 subgrids for duplicates
    for i in range(0, 16, 4):
        for j in range(0, 16, 4):
            block = [board[x][y] for x in range(i, i + 4) for y in range(j, j + 4)]
            if not is_valid_block(block):
                return False, "Duplicate number in 4x4 subgrid"

    # Check for completeness
    if incomplete:
        return False, "Sudoku board is incomplete"

    return True, "Valid and complete Sudoku board"


def check_data_types(board):
    # Check if board is a list of lists
    if not isinstance(board, list) or not all(isinstance(row, list) for row in board):
        return False, "Board is not a list of lists"

    # Check dimensions of the board
    if len(board) != 16 or any(len(row) != 16 for row in board):
        return False, "Board dimensions are not 16x16"

    # Check data types of each cell
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if not isinstance(cell, int):
                return False, f"Cell at ({i + 1}, {j + 1}) is not an integer"

    return True, "Valid board"

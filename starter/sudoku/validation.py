from .constants import SIZE


def is_safe(board, row, col, num):
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def get_move_conflicts(board, row, col, num):
    original_value = board[row][col]
    board[row][col] = 0
    conflicts = []

    if any(board[row][x] == num for x in range(SIZE)):
        conflicts.append("row")
    if any(board[x][col] == num for x in range(SIZE)):
        conflicts.append("column")

    start_row = row - row % 3
    start_col = col - col % 3
    if any(
        board[start_row + i][start_col + j] == num
        for i in range(3)
        for j in range(3)
    ):
        conflicts.append("box")

    board[row][col] = original_value
    return conflicts


def validate_move(board, row, col, num):
    conflicts = get_move_conflicts(board, row, col, num)
    return {
        "valid": len(conflicts) == 0,
        "conflicts": conflicts,
    }


def get_move_conflicts(board, row, col, num):
    conflicts = []

    # Ignore the current cell value when validating a move.
    board_value = board[row][col]
    board[row][col] = 0

    if any(board[row][x] == num for x in range(SIZE)):
        conflicts.append("row")

    if any(board[x][col] == num for x in range(SIZE)):
        conflicts.append("column")

    start_row = row - row % 3
    start_col = col - col % 3
    if any(
        board[start_row + i][start_col + j] == num
        for i in range(3)
        for j in range(3)
    ):
        conflicts.append("box")

    board[row][col] = board_value
    return conflicts


def validate_move(board, row, col, num):
    conflicts = get_move_conflicts(board, row, col, num)
    return {
        "valid": len(conflicts) == 0,
        "conflicts": conflicts,
    }

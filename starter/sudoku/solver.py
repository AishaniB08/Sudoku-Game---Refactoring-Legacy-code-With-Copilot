import random

from .validation import is_safe
from .constants import EMPTY, SIZE


def find_empty_cell(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                return row, col
    return None, None


def count_solutions(board, limit=2):
    row, col = find_empty_cell(board)
    if row is None:
        return 1

    solutions = 0
    for candidate in range(1, SIZE + 1):
        if is_safe(board, row, col, candidate):
            board[row][col] = candidate
            solutions += count_solutions(board, limit)
            board[row][col] = EMPTY
            if solutions >= limit:
                return solutions
    return solutions


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

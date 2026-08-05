import random

from .board import create_empty_board, deep_copy
from .constants import EMPTY, SIZE
from .solver import count_solutions, fill_board

DIFFICULTY_CLUES = {
    "easy": 45,
    "medium": 35,
    "hard": 28,
}


def _clues_for_difficulty(difficulty):
    if difficulty is None:
        difficulty = "medium"
    difficulty = str(difficulty).lower()
    try:
        return DIFFICULTY_CLUES[difficulty]
    except KeyError as exc:
        raise ValueError(
            "Invalid difficulty %r. Expected one of: %s." % (
                difficulty,
                ", ".join(DIFFICULTY_CLUES.keys()),
            )
        ) from exc


def remove_cells(board, clues):
    cells = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(cells)
    removed = 0
    max_removals = SIZE * SIZE - clues

    for row, col in cells:
        if removed >= max_removals:
            break
        if board[row][col] == EMPTY:
            continue

        backup = board[row][col]
        board[row][col] = EMPTY

        if count_solutions(board, limit=2) != 1:
            board[row][col] = backup
        else:
            removed += 1


def generate_puzzle(clues=None, difficulty="medium"):
    if clues is None:
        clues = _clues_for_difficulty(difficulty)
    elif difficulty is not None and difficulty != "medium":
        raise ValueError(
            "Use either clues or difficulty, not both. "
            "Received clues=%r and difficulty=%r." % (clues, difficulty)
        )

    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution

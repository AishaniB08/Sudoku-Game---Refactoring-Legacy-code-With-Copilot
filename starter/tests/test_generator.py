import pytest
import sudoku


def test_generate_puzzle_returns_puzzle_and_solution():
    puzzle, solution = sudoku.generate_puzzle(clues=81)

    assert puzzle == solution
    assert len(puzzle) == sudoku.SIZE
    assert all(len(row) == sudoku.SIZE for row in puzzle)
    assert all(cell != sudoku.EMPTY for row in puzzle for cell in row)


def test_generate_puzzle_uses_difficulty_mapping():
    easy_puzzle, _ = sudoku.generate_puzzle(difficulty="easy")
    medium_puzzle, _ = sudoku.generate_puzzle(difficulty="medium")
    hard_puzzle, _ = sudoku.generate_puzzle(difficulty="hard")

    easy_clues = sum(1 for row in easy_puzzle for cell in row if cell != sudoku.EMPTY)
    medium_clues = sum(1 for row in medium_puzzle for cell in row if cell != sudoku.EMPTY)
    hard_clues = sum(1 for row in hard_puzzle for cell in row if cell != sudoku.EMPTY)

    assert easy_clues >= medium_clues >= hard_clues
    assert easy_clues == 45
    assert medium_clues == 35
    assert hard_clues == 28


def test_generate_puzzle_rejects_invalid_difficulty():
    with pytest.raises(ValueError, match="Invalid difficulty"):
        sudoku.generate_puzzle(difficulty="expert")


def test_remove_cells_leaves_at_least_target_clues_and_unique_solution():
    board = sudoku.create_empty_board()
    sudoku.fill_board(board)
    sudoku.remove_cells(board, clues=35)

    filled_cells = sum(1 for row in board for cell in row if cell != sudoku.EMPTY)
    assert filled_cells >= 35
    assert sudoku.count_solutions(board, limit=2) == 1

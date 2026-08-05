import sudoku


def test_create_empty_board_returns_empty_9x9_grid():
    board = sudoku.create_empty_board()

    assert len(board) == sudoku.SIZE
    assert all(len(row) == sudoku.SIZE for row in board)
    assert all(cell == sudoku.EMPTY for row in board for cell in row)


def test_deep_copy_returns_independent_copy():
    board = sudoku.create_empty_board()
    board_copy = sudoku.deep_copy(board)

    board_copy[0][0] = 1
    assert board[0][0] == sudoku.EMPTY
    assert board_copy[0][0] == 1

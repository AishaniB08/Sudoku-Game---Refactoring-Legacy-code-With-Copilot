import sudoku


def test_is_safe_rejects_row_conflict():
    board = sudoku.create_empty_board()
    board[0][0] = 4

    assert not sudoku.is_safe(board, 0, 1, 4)


def test_is_safe_rejects_column_conflict():
    board = sudoku.create_empty_board()
    board[0][1] = 6

    assert not sudoku.is_safe(board, 1, 1, 6)


def test_is_safe_rejects_box_conflict():
    board = sudoku.create_empty_board()
    board[0][0] = 7

    assert not sudoku.is_safe(board, 1, 1, 7)


def test_is_safe_allows_safe_number():
    board = sudoku.create_empty_board()
    board[0][0] = 1

    assert sudoku.is_safe(board, 0, 1, 2)

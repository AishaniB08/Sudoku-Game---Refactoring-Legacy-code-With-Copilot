import sudoku


def test_fill_board_completes_empty_board():
    board = sudoku.create_empty_board()

    assert sudoku.fill_board(board) is True
    assert all(cell != sudoku.EMPTY for row in board for cell in row)


def test_filled_board_has_valid_rows_columns_and_boxes():
    board = sudoku.create_empty_board()
    sudoku.fill_board(board)

    for row in board:
        assert set(row) == set(range(1, sudoku.SIZE + 1))

    for col in range(sudoku.SIZE):
        column = [board[row][col] for row in range(sudoku.SIZE)]
        assert set(column) == set(range(1, sudoku.SIZE + 1))

    for box_row in range(0, sudoku.SIZE, 3):
        for box_col in range(0, sudoku.SIZE, 3):
            box = [
                board[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            assert set(box) == set(range(1, sudoku.SIZE + 1))


def test_count_solutions_returns_one_for_puzzle_with_single_empty_cell():
    board = sudoku.create_empty_board()
    sudoku.fill_board(board)
    board[0][0] = sudoku.EMPTY

    assert sudoku.count_solutions(board, limit=2) == 1


def test_count_solutions_stops_at_two_solutions():
    board = sudoku.create_empty_board()

    assert sudoku.count_solutions(board, limit=2) == 2

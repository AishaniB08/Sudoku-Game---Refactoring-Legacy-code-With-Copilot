import sudoku_logic


def test_create_empty_board_returns_9x9_empty_board():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_returns_independent_board_copy():
    board = sudoku_logic.create_empty_board()
    copy_board = sudoku_logic.deep_copy(board)

    copy_board[0][0] = 1
    assert board[0][0] == sudoku_logic.EMPTY
    assert copy_board[0][0] == 1


def test_is_safe_detects_conflicts_in_row_column_and_box():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[1][3] = 7
    board[2][1] = 8

    assert not sudoku_logic.is_safe(board, 0, 1, 5)
    assert not sudoku_logic.is_safe(board, 2, 0, 5)
    assert not sudoku_logic.is_safe(board, 1, 2, 5)
    assert sudoku_logic.is_safe(board, 0, 1, 6)


def test_fill_board_produces_valid_complete_sudoku():
    board = sudoku_logic.create_empty_board()
    assert sudoku_logic.fill_board(board) is True

    assert all(cell != sudoku_logic.EMPTY for row in board for cell in row)

    for row in board:
        assert set(row) == set(range(1, sudoku_logic.SIZE + 1))

    for col in range(sudoku_logic.SIZE):
        column = [board[row][col] for row in range(sudoku_logic.SIZE)]
        assert set(column) == set(range(1, sudoku_logic.SIZE + 1))

    for box_row in range(0, sudoku_logic.SIZE, 3):
        for box_col in range(0, sudoku_logic.SIZE, 3):
            box = [
                board[r][c]
                for r in range(box_row, box_row + 3)
                for c in range(box_col, box_col + 3)
            ]
            assert set(box) == set(range(1, sudoku_logic.SIZE + 1))


def test_generate_puzzle_returns_solution_and_puzzle_with_matching_full_board_when_clues_equal_81():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=81)

    assert puzzle == solution
    assert all(cell != sudoku_logic.EMPTY for row in puzzle for cell in row)
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)

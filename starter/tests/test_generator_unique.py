import sudoku


def test_generate_puzzle_has_single_solution_for_clues_81():
    puzzle, _ = sudoku.generate_puzzle(clues=81)
    assert sudoku.count_solutions(puzzle, limit=2) == 1


def test_generate_puzzle_stops_removal_on_unique_solution():
    puzzle, _ = sudoku.generate_puzzle(clues=35)
    assert sudoku.count_solutions(puzzle, limit=2) == 1

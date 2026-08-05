from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'hints': 0,
    'difficulty': 'medium',
}

LEADERBOARD = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium')
    clues = int(request.args.get('clues', 35))
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['hints'] = 0
    CURRENT['difficulty'] = difficulty
    return jsonify({
        'puzzle': puzzle,
        'hints': CURRENT['hints'],
        'difficulty': CURRENT['difficulty'],
    })

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    return jsonify({'leaderboard': LEADERBOARD})

@app.route('/submit-score', methods=['POST'])
def submit_score():
    data = request.json
    name = (data.get('name') or '').strip()
    time_seconds = data.get('time')
    difficulty = data.get('difficulty') or CURRENT.get('difficulty', 'medium')
    hints = data.get('hints')

    if not name:
        return jsonify({'error': 'Player name is required.'}), 400

    try:
        time_seconds = int(time_seconds)
        hints = int(hints)
    except (TypeError, ValueError):
        return jsonify({'error': 'Time and hints must be numeric.'}), 400

    score = {
        'name': name,
        'time': time_seconds,
        'difficulty': difficulty,
        'hints': hints,
    }

    LEADERBOARD.append(score)
    LEADERBOARD.sort(key=lambda item: item['time'])
    del LEADERBOARD[10:]

    return jsonify({'leaderboard': LEADERBOARD})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({
        'incorrect': incorrect,
        'hints': CURRENT['hints'],
    })


@app.route('/hint', methods=['POST'])
def hint_cell():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    empty_cells = [
        (i, j)
        for i in range(sudoku_logic.SIZE)
        for j in range(sudoku_logic.SIZE)
        if puzzle[i][j] == 0
    ]

    if not empty_cells:
        return jsonify({'error': 'No empty cells available for a hint'}), 400

    row, col = empty_cells[0]
    value = solution[row][col]
    puzzle[row][col] = value
    CURRENT['hints'] += 1

    return jsonify({
        'row': row,
        'col': col,
        'value': value,
        'hints': CURRENT['hints'],
    })


@app.route('/validate-move', methods=['POST'])
def validate_move_endpoint():
    data = request.json
    board = data.get('board')
    row = data.get('row')
    col = data.get('col')
    value = data.get('value')

    if board is None or row is None or col is None or value is None:
        return jsonify({'error': 'Missing board, row, col, or value'}), 400

    try:
        row = int(row)
        col = int(col)
        value = int(value)
    except (TypeError, ValueError):
        return jsonify({'error': 'Row, col, and value must be integers'}), 400

    if not (0 <= row < sudoku_logic.SIZE and 0 <= col < sudoku_logic.SIZE):
        return jsonify({'error': 'Row and column must be between 0 and 8'}), 400
    if not (1 <= value <= sudoku_logic.SIZE):
        return jsonify({'error': 'Value must be between 1 and 9'}), 400

    validation = sudoku_logic.validate_move(board, row, col, value)
    return jsonify(validation)

if __name__ == '__main__':
    app.run(debug=True)
# GitHub Copilot Instructions for Flask Sudoku Refactoring

## Objective
Refactor the Flask Sudoku application to be modular, maintainable, and testable while preserving existing functionality and user experience.

## Key goals
- Separate Sudoku game logic from Flask UI and request handling.
- Keep the current game flow and browser-facing behavior unchanged.
- Use Flask best practices for routing, request handling, and application structure.
- Write clear, concise comments for major functions and modules.
- Add pytest-compatible tests for Sudoku logic and key Flask endpoints.

## Project structure guidance
- Keep Flask application code in `app.py` or a dedicated application module.
- Move Sudoku-specific logic into a separate module, e.g. `sudoku_logic.py`.
- Keep HTML templates in `templates/` and client assets in `static/`.
- Avoid mixing game rules, board generation, and validation directly inside route handlers.

## Coding expectations
- Implement pure Sudoku functions in `sudoku_logic.py` such as:
  - puzzle generation
  - valid move checking
  - board validation / solution checking
  - hint generation
- In Flask routes, call those functions but do not reimplement Sudoku rules.
- Use Python naming conventions and keep functions small and focused.
- Add docstrings or comments explaining why a function exists, not just what it does.

## Flask best practices
- Use `@app.route(...)` for route definitions.
- Keep route handlers responsible only for:
  - parsing request data
  - calling business logic
  - returning JSON or rendering templates
- Avoid storing persistent game state on the server beyond what is needed for a single request.
- Handle invalid input gracefully and return helpful JSON error messages.

## Testing with pytest
- Add tests in a `tests/` folder or a `test_*.py` file.
- Write unit tests for Sudoku logic:
  - valid move checks
  - puzzle validation
  - hint generation
  - solution correctness
- Write integration-style tests for Flask routes if possible using Flask test client.
- Ensure tests cover both normal and edge-case behavior.

## Preservation requirements
- Do not remove or break existing features such as:
  - generating a new puzzle
  - validating moves
  - checking the board
  - requesting hints
  - leaderboard persistence and submission
- Keep the frontend and backend contract intact so existing JavaScript calls continue to work.

## Style notes
- Be explicit about separation of concerns.
- Prefer reusable helper functions over repeated logic.
- Keep the code clear and maintainable for future updates.

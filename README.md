# Sudoku Game – Refactoring Legacy Code with GitHub Copilot

## Project Overview

This project is a web-based Sudoku game built using **Python Flask** as part of the **Refactoring Legacy Code with GitHub Copilot** project.

The objective of this project is to modernize and improve an existing legacy Sudoku application by refactoring the code into a modular structure, implementing new gameplay features, enhancing the user interface, and demonstrating the responsible use of GitHub Copilot throughout the development process.

GitHub Copilot was used as an AI programming assistant to help with code generation, refactoring, testing, debugging, and documentation. All AI-generated code was reviewed, modified, or rejected where necessary to ensure correctness and maintainability.

---

## Features

### Core Sudoku Features

- Generate valid Sudoku puzzles
- Ensure every generated puzzle has exactly one unique solution
- Easy, Medium, and Hard difficulty levels
- Locked prefilled cells
- Immediate validation of player moves
- Congratulations message upon successful completion

### Gameplay Features

- Hint button (fills one correct cell and locks it)
- Check button (highlights incorrect entries)
- Game timer
- Top 10 leaderboard
- Persistent leaderboard using browser Local Storage
- Dark Mode toggle

### User Interface

- Responsive design for desktop and mobile devices
- Alternating colors for each 3×3 Sudoku region
- Clean and intuitive interface
- Light and Dark theme support

### Code Quality

- Refactored legacy code into modular components
- Reusable functions
- Clear project structure
- Error handling
- Unit testing with Pytest

---

## Technologies Used

- Python 3
- Flask
- HTML5
- CSS3
- JavaScript
- Git
- GitHub
- GitHub Copilot
- Pytest

---

## Project Structure

```
starter/
│
├── app.py
├── sudoku_logic.py
├── requirements.txt
├── README.md
├── instruction.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── styles.css
│   └── main.js
│
├── tests/
│
└── Screenshots/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/AishaniB08/Sudoku-Game---Refactoring-Legacy-code-With-Copilot.git
```

Navigate to the project folder:

```bash
cd starter
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Running the Tests

Install Pytest if necessary:

```bash
pip install pytest
```

Run the test suite:

```bash
pytest
```

---

## GitHub Copilot Usage

GitHub Copilot was used throughout the project to assist with:

- Setting up the testing framework
- Refactoring legacy code
- Generating Sudoku puzzles with a unique solution
- Implementing difficulty levels
- Creating Hint and Check features
- Building the leaderboard
- Implementing Local Storage
- Styling the Sudoku grid
- Supporting Dark Mode
- Improving documentation

All generated suggestions were reviewed before being accepted, modified when necessary, and rejected when they did not meet the project requirements.

---

## Screenshots

The project includes a **Screenshots** folder containing Copilot conversations and project milestones, including:

- Testing framework setup
- Unique solution generation
- Difficulty selector
- Immediate validation
- Hint and Check implementation
- Leaderboard and Local Storage
- Grid styling
- Dark Mode implementation

---

## Future Improvements

Possible future enhancements include:

- Note Mode (candidate numbers)
- Sudoku solver animation
- WCAG 2.1 AA accessibility improvements
- Keyboard shortcuts
- Undo/Redo functionality
- Additional puzzle themes
- Online leaderboard
- Multiple board sizes

---

## License

This project is developed for educational purposes as part of the **GitHub Copilot: Refactoring Legacy Code** assignment.

// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_STORAGE_KEY = 'sudokuLeaderboard';
const THEME_STORAGE_KEY = 'sudokuTheme';
let puzzle = [];
let timerInterval = null;
let timerStart = null;
let elapsedSeconds = 0;
let currentDifficulty = 'medium';

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60).toString().padStart(2, '0');
  const secs = (seconds % 60).toString().padStart(2, '0');
  return `${minutes}:${secs}`;
}

function updateTimerDisplay(seconds) {
  document.getElementById('timer').innerText = formatTime(seconds);
}

function startTimer() {
  stopTimer();
  timerStart = Date.now() - elapsedSeconds * 1000;
  updateTimerDisplay(elapsedSeconds);
  timerInterval = setInterval(() => {
    elapsedSeconds = Math.floor((Date.now() - timerStart) / 1000);
    updateTimerDisplay(elapsedSeconds);
  }, 1000);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function resetTimer() {
  stopTimer();
  elapsedSeconds = 0;
  updateTimerDisplay(0);
}

function getBoardState() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-mode', isDark);
  const checkbox = document.getElementById('theme-toggle');
  if (checkbox) {
    checkbox.checked = isDark;
  }
  localStorage.setItem(THEME_STORAGE_KEY, theme);
}

function initializeTheme() {
  const storedTheme = localStorage.getItem(THEME_STORAGE_KEY);
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  const theme = storedTheme || (prefersDark ? 'dark' : 'light');
  applyTheme(theme);
}

function loadStoredLeaderboard() {
  const raw = localStorage.getItem(LEADERBOARD_STORAGE_KEY);
  if (!raw) {
    return [];
  }
  try {
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.warn('Failed to parse stored leaderboard:', error);
    return [];
  }
}

function saveLeaderboard(entries) {
  const topScores = entries.slice(0, 10);
  localStorage.setItem(LEADERBOARD_STORAGE_KEY, JSON.stringify(topScores));
}

async function validateCellMove(input) {
  const row = parseInt(input.dataset.row, 10);
  const col = parseInt(input.dataset.col, 10);
  const value = input.value ? parseInt(input.value, 10) : 0;
  if (!value) {
    input.classList.remove('incorrect');
    return true;
  }

  const board = getBoardState();
  const res = await fetch('/validate-move', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board, row, col, value}),
  });
  const data = await res.json();
  if (data.valid) {
    input.classList.remove('incorrect');
    return true;
  }
  input.classList.add('incorrect');
  return false;
}

async function revalidateIncorrectCells() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const incorrectInputs = Array.from(inputs).filter(
    (inp) => inp.classList.contains('incorrect') && inp.value
  );
  await Promise.all(incorrectInputs.map((input) => validateCellMove(input)));
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      const regionRow = Math.floor(i / 3);
      const regionCol = Math.floor(j / 3);
      const regionClass = (regionRow + regionCol) % 2 === 0 ? 'region-light' : 'region-dark';
      input.className = `sudoku-cell ${regionClass}`;
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', async (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        if (!val) {
          e.target.classList.remove('incorrect');
        } else {
          await validateCellMove(e.target);
        }
        await revalidateIncorrectCells();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function updateHintButtonState(board) {
  const hintButton = document.getElementById('use-hint');
  const hasEmptyCell = board.some((row) => row.some((value) => value === 0));
  hintButton.disabled = !hasEmptyCell;
}

function updateHintsUsed(count) {
  document.getElementById('hints-used').innerText = `Hints used: ${count}`;
}

async function newGame() {
  const res = await fetch('/new');
  const data = await res.json();
  currentDifficulty = data.difficulty || 'medium';
  renderPuzzle(data.puzzle);
  updateHintsUsed(data.hints ?? 0);
  updateHintButtonState(data.puzzle);
  resetTimer();
  startTimer();
  renderLeaderboard(loadStoredLeaderboard());
  document.getElementById('message').innerText = '';
}

async function useHint() {
  const res = await fetch('/hint', {
    method: 'POST',
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }

  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = data.row * SIZE + data.col;
  const input = inputs[idx];
  input.value = data.value;
  input.disabled = true;
  input.classList.add('hint');
  puzzle[data.row][data.col] = data.value;

  updateHintsUsed(data.hints);
  updateHintButtonState(puzzle);
  msg.style.color = '#388e3c';
  msg.innerText = 'Hint applied to one empty cell.';
}

async function submitScore(name, time, difficulty, hints) {
  const res = await fetch('/submit-score', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name, time, difficulty, hints}),
  });
  const data = await res.json();
  if (data.error) {
    return {error: data.error};
  }
  if (Array.isArray(data.leaderboard)) {
    saveLeaderboard(data.leaderboard);
    renderLeaderboard(data.leaderboard);
  }
  return data;
}

function renderLeaderboard(entries) {
  const tbody = document.querySelector('#leaderboard-table tbody');
  tbody.innerHTML = '';
  entries.forEach((entry, index) => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${entry.name}</td>
      <td>${formatTime(entry.time)}</td>
      <td>${entry.difficulty}</td>
      <td>${entry.hints}</td>
    `;
    tbody.appendChild(row);
  });
}

async function fetchLeaderboard() {
  const stored = loadStoredLeaderboard();
  renderLeaderboard(stored);
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.classList.remove('incorrect');
    const val = inp.value;
    if (val && incorrect.has(idx)) {
      inp.classList.add('incorrect');
    }
  }
  if (incorrect.size === 0) {
    stopTimer();
    let playerName = document.getElementById('player-name').value.trim();
    if (!playerName) {
      playerName = window.prompt('Congratulations! Enter your name to save your score:', 'Player');
      if (playerName) {
        playerName = playerName.trim();
        document.getElementById('player-name').value = playerName;
      }
    }

    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! You solved it!';

    if (playerName) {
      const result = await submitScore(playerName, elapsedSeconds, currentDifficulty, data.hints || 0);
      if (!result.error) {
        renderLeaderboard(result.leaderboard || []);
      }
    } else {
      msg.innerText += ' Enter your name to save the score to the leaderboard.';
    }
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('use-hint').addEventListener('click', useHint);
  const themeToggle = document.getElementById('theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('change', () => {
      applyTheme(themeToggle.checked ? 'dark' : 'light');
    });
  }
  initializeTheme();
  // initialize
  newGame();
});
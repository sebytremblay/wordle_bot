# Wordle Solver

An intelligent Wordle solver system that implements multiple search algorithms to solve Wordle puzzles efficiently.

## Features

- Multiple solver implementations:
  - Naive Solver: Random selection from filtered candidates
  - Greedy Solver: Information gain-based selection (coming soon)
  - Minimax Solver: Alpha-beta pruning for worst-case optimization (coming soon)
  - MCTS Solver: Monte Carlo Tree Search for probabilistic optimization (coming soon)
- Web API for game interaction
- Detailed feedback processing and candidate filtering
- Support for custom word dictionaries

## Installation

### General

1. Clone the repository:
```bash
git clone <repository-url>
cd wordle-solver
```

### Backend


1. Open backend directory
```bash
cd backend/
```

2. Create a virtual environment and activate it:
```bash
virtualenv venv
source venv/bin/activate
```

3.. Install dependencies:
```bash
pip install -r requirements.txt
```

### Frontend

1. Open frontend directory
```bash
cd frontend/
```

2. Install dependencies
```bash
npm install
```

## Usage

### Running the Web Server

1. Start the API
```bash
cd backend/
python main.py
```

2. Run the frontend
```bash
cd frontend/
npm run start
```

The API server will start on `http://localhost:3001` and the web interface will run on `http://loclahost:3000` by default.

### Running Locally

If you want to run the solvers locally, use [backend/playground.py](backend/playground.py) as reference for how to simulate different solvers.

## Development

### Adding a New Solver

1. Create a new solver class in `wordle_game/solver/` that inherits from `BaseSolver`
2. Implement the `select_guess()` method

Example:
```python
from .base_solver import BaseSolver

class MyNewSolver(BasdseSolver):
    def select_guess(self) -> str:
        # Implement your guess selection logic here
        pass
```
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

1. Clone the repository:
```bash
git clone <repository-url>
cd wordle-solver
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Server

```bash
python -m web_interface.app
```

The server will start on `http://localhost:5000` by default.

### API Endpoints

1. Start a new game:
```bash
curl -X POST http://localhost:5000/newgame \
  -H "Content-Type: application/json" \
  -d '{"solver": "naive"}'
```

2. Make a guess:
```bash
curl -X POST http://localhost:5000/guess \
  -H "Content-Type: application/json" \
  -d '{"guess": "hello"}'
```

3. Get a hint:
```bash
curl http://localhost:5000/hint
```

## Project Structure

```
project/
├── README.md
├── requirements.txt
├── main.py
├── config.py
│
├── wordle_game/
│   ├── __init__.py
│   ├── wordle_game.py
│   ├── dictionary.py
│   ├── feedback.py
│   └── solver/
│       ├── __init__.py
│       ├── base_solver.py
│       ├── naive_solver.py
│       ├── greedy_solver.py
│       ├── minimax_solver.py
│       └── mcts_solver.py
│
└── web_interface/
    ├── __init__.py
    ├── app.py
    └── templates/
```

## Dictionary Format

The system supports two dictionary file formats:

1. Text file (one word per line):
```
hello
world
about
...
```

2. JSON file:
```json
{
  "words": [
    "hello",
    "world",
    "about",
    ...
  ]
}
```

## Development

### Adding a New Solver

1. Create a new solver class in `wordle_game/solver/` that inherits from `BaseSolver`
2. Implement the `select_guess()` method
3. Register the solver in `web_interface/app.py`

Example:
```python
from .base_solver import BaseSolver

class MyNewSolver(BaseSolver):
    def select_guess(self) -> str:
        # Implement your guess selection logic here
        pass
```

## License

MIT License 
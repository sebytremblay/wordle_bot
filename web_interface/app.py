from flask import Flask, request, jsonify
from typing import Dict, Any, Optional
import os
import json

from wordle_game.wordle_game import WordleGame
from wordle_game.dictionary import load_dictionary
from wordle_game.solver import (
    NaiveSolver,
    GreedySolver,
    MinimaxSolver,
    MCTSSolver
)

app = Flask(__name__)

# Global state (in a real app, use proper session management)
GAMES: Dict[str, WordleGame] = {}
SOLVERS: Dict[str, Any] = {}

# Load dictionary
DICTIONARY_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'words.txt')
try:
    WORD_LIST = load_dictionary(DICTIONARY_PATH)
except FileNotFoundError:
    # Fallback to a small test dictionary if file not found
    WORD_LIST = ["hello", "world", "about", "above", "abuse", "actor", "acute", "admit",
                 "adopt", "adult", "after", "again", "agent", "agree", "ahead", "alarm"]


def get_solver(solver_type: str, dictionary: list) -> Any:
    """Get a solver instance based on the specified type."""
    solvers = {
        "naive": NaiveSolver,
        "greedy": GreedySolver,
        "minimax": MinimaxSolver,
        "mcts": MCTSSolver
    }

    solver_class = solvers.get(solver_type.lower())
    if not solver_class:
        raise ValueError(f"Unknown solver type: {solver_type}")

    # Handle special initialization for different solvers
    if solver_class == MinimaxSolver:
        return solver_class(dictionary, max_depth=3)
    elif solver_class == MCTSSolver:
        return solver_class(dictionary, simulations=1000)
    else:
        return solver_class(dictionary)


@app.route('/newgame', methods=['POST'])
def new_game():
    """Start a new game with optional solver selection."""
    data = request.get_json() or {}
    game_id = data.get('game_id', 'default')
    solver_type = data.get('solver', 'naive')

    # Create new game instance
    game = WordleGame(WORD_LIST)
    game.start_new_game()
    GAMES[game_id] = game

    # Create solver if requested
    if solver_type:
        try:
            SOLVERS[game_id] = get_solver(solver_type, WORD_LIST)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({
        'game_id': game_id,
        'solver_type': solver_type,
        'state': game.get_game_state()
    })


@app.route('/guess', methods=['POST'])
def make_guess():
    """Submit a guess for the current game."""
    data = request.get_json()
    if not data or 'guess' not in data:
        return jsonify({'error': 'No guess provided'}), 400

    game_id = data.get('game_id', 'default')
    game = GAMES.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    try:
        feedback, is_game_over = game.submit_guess(data['guess'])

        # Update solver if one exists for this game
        solver = SOLVERS.get(game_id)
        if solver:
            solver.update(data['guess'], feedback)

        return jsonify({
            'feedback': feedback,
            'state': game.get_game_state()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/hint', methods=['GET'])
def get_hint():
    """Get a hint from the current solver."""
    game_id = request.args.get('game_id', 'default')

    game = GAMES.get(game_id)
    solver = SOLVERS.get(game_id)

    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if not solver:
        return jsonify({'error': 'No solver available'}), 400
    if game.is_game_over():
        return jsonify({'error': 'Game is already over'}), 400

    try:
        hint = solver.select_guess()
        return jsonify({
            'hint': hint,
            'candidates_remaining': solver.get_candidate_count()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/solvers', methods=['GET'])
def list_solvers():
    """List available solver types."""
    return jsonify({
        'solvers': [
            {
                'id': 'naive',
                'name': 'Naive Solver',
                'description': 'Randomly selects from remaining candidates'
            },
            {
                'id': 'greedy',
                'name': 'Greedy Solver',
                'description': 'Uses information gain to select optimal guesses'
            },
            {
                'id': 'minimax',
                'name': 'Minimax Solver',
                'description': 'Uses alpha-beta pruning to minimize worst-case scenarios'
            },
            {
                'id': 'mcts',
                'name': 'MCTS Solver',
                'description': 'Uses Monte Carlo Tree Search for probabilistic optimization'
            }
        ]
    })


if __name__ == '__main__':
    app.run(debug=True)

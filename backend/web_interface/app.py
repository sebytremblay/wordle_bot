import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, Any, Optional
import os
import json

from wordle_game.wordle_game import WordleGame
from wordle_game.dictionary import load_dictionary

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],  # React development server
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Global state (in a real app, use proper session management)
GAMES: Dict[str, WordleGame] = {}

# Load dictionary
DICTIONARY_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'data', 'words.txt')
try:
    WORD_LIST = load_dictionary(DICTIONARY_PATH)
except FileNotFoundError:
    # Fallback to a small test dictionary if file not found
    WORD_LIST = ["hello", "world", "about", "above", "abuse", "actor", "acute", "admit",
                 "adopt", "adult", "after", "again", "agent", "agree", "ahead", "alarm"]


@app.route('/newgame', methods=['POST'])
def new_game():
    """Start a new game with optional solver selection."""
    data = request.get_json() or {}
    game_id = str(uuid.uuid4())
    solver_type = data.get('solver', 'naive')

    # Create new game instance
    game = WordleGame(WORD_LIST)
    game.start_new_game()
    GAMES[game_id] = game

    # Initialize solver if requested
    if solver_type:
        try:
            game.solver_manager.get_solver(solver_type)
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
        return jsonify({
            'feedback': feedback,
            'state': game.get_game_state()
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/hint', methods=['GET'])
def get_hint():
    """Get a hint from a solver."""
    game_id = request.args.get('game_id', 'default')
    solver_type = request.args.get('solver')  # Optional parameter

    game = GAMES.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    if game.is_game_over():
        return jsonify({'error': 'Game is already over'}), 400

    try:
        # Get or switch to requested solver
        if solver_type:
            solver = game.solver_manager.get_solver(solver_type)
        else:
            solver = game.solver_manager.get_active_solver()
            if not solver:
                # No active solver, default to naive
                solver = game.solver_manager.get_solver('naive')

        hint = solver.select_guess()
        return jsonify({
            'hint': hint,
            'solver_type': solver.solver_type,
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

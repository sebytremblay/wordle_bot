import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict
import config

from web_interface.app_session import AppSession
from wordle_game.dictionary import load_dictionary
from cache_service.hint_cache import HintCache, SupabaseConnectionError, HintCacheError

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:3000"],  # React development server
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Global state (in a real app, use proper session management)
SESSIONS: Dict[str, AppSession] = {}

# Load dictionary
word_list = load_dictionary(config.DICTIONARY_PATH)


@app.route('/newgame', methods=['POST'])
def new_game():
    """Start a new game with optional solver selection."""
    data = request.get_json() or {}
    game_id = str(uuid.uuid4())
    solver_type = data.get('solver', config.DEFAULT_SOLVER)

    # Create new game session
    session = AppSession(word_list)
    SESSIONS[game_id] = session

    # Initialize solver if requested
    if solver_type:
        try:
            session.solver_manager.get_solver(solver_type)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({
        'game_id': game_id,
        'solver_type': solver_type,
        'state': session.get_game_state()
    })


@app.route('/guess', methods=['POST'])
def make_guess():
    """Submit a guess for the current game."""
    data = request.get_json()
    if not data or 'guess' not in data:
        return jsonify({'error': 'No guess provided'}), 400

    game_id = data.get('game_id', 'default')
    session = SESSIONS.get(game_id)
    if not session:
        return jsonify({'error': 'Game not found'}), 404

    try:
        feedback, _ = session.submit_guess(data['guess'])
        return jsonify({
            'feedback': feedback,
            'state': session.get_game_state(),
            'game_id': game_id
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/hint', methods=['GET'])
def get_hint():
    """Get a hint from a solver with caching support."""
    game_id = request.args.get('game_id', 'default')
    solver_type = request.args.get(
        'solver', config.DEFAULT_SOLVER)

    session = SESSIONS.get(game_id)
    if not session:
        return jsonify({'error': 'Game not found'}), 404
    if session.is_game_over():
        return jsonify({'error': 'Game is already over'}), 400

    try:
        # Get current game state
        game_state = session.get_game_state()

        # Define hint computation function
        def compute_hint():
            hint, _, _ = session.get_hint(solver_type)
            return hint

        # Try to get cached hint or compute new one
        try:
            hint, was_cached = HintCache.get_or_compute_hint(
                game_state=game_state,
                solver_type=solver_type,
                compute_fn=compute_hint
            )
        except (SupabaseConnectionError, HintCacheError) as e:
            # If caching fails, fall back to direct computation
            app.logger.error(f"Cache error: {str(e)}")
            hint = compute_hint()
            was_cached = False

        return jsonify({
            'hint': hint,
            'solver_type': solver_type,
            'cached': was_cached,
            'game_id': game_id
        })

    except Exception as e:
        app.logger.error(f"Error getting hint: {str(e)}")
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
                'id': f'minimax_{config.MINIMAX_DEPTH}',
                'name': 'Minimax Solver',
                'description': 'Uses alpha-beta pruning to minimize worst-case scenarios'
            },
            {
                'id': f'mcts_{config.MCTS_SIMULATIONS}',
                'name': 'MCTS Solver',
                'description': 'Uses Monte Carlo Tree Search for probabilistic optimization'
            }
        ]
    })


@app.route('/remaining-words', methods=['GET'])
def get_remaining_words():
    """Get the list of remaining candidate words."""
    game_id = request.args.get('game_id', 'default')
    session = SESSIONS.get(game_id)
    if not session:
        return jsonify({'error': 'Game not found'}), 404

    remaining_words = session.get_remaining_candidates()
    return jsonify({
        'words': remaining_words,
        'count': len(remaining_words)
    })


@app.route('/mirrorgame', methods=['POST'])
def mirror_game():
    """Create a new game with the same target word as an existing game."""
    data = request.get_json()
    if not data or 'game_id' not in data:
        return jsonify({'error': 'No game_id provided'}), 400

    original_session = SESSIONS.get(data['game_id'])
    if not original_session:
        return jsonify({'error': 'Original game not found'}), 404

    # Create new game with same target word
    new_game_id = str(uuid.uuid4())
    new_session = AppSession(
        word_list, target_word=original_session.game_state.target_word)
    SESSIONS[new_game_id] = new_session

    # Initialize solver if requested
    solver_type = data.get('solver', config.DEFAULT_SOLVER)
    if solver_type:
        try:
            new_session.solver_manager.get_solver(solver_type)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    return jsonify({
        'game_id': new_game_id,
        'solver_type': solver_type,
        'state': new_session.get_game_state()
    })


if __name__ == '__main__':
    app.run(debug=True)

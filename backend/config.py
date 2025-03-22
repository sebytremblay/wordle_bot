"""
Configuration settings for the Wordle solver application.
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_config() -> Dict[str, Any]:
    """
    Get configuration settings from environment variables.

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    return {
        'flask': {
            'app': os.getenv('FLASK_APP', 'main.py'),
            'env': os.getenv('FLASK_ENV', 'development'),
            'debug': os.getenv('FLASK_DEBUG', '1') == '1'
        },
        'server': {
            'host': os.getenv('HOST', '0.0.0.0'),
            'port': int(os.getenv('PORT', '3001')),
            'debug': os.getenv('DEBUG', 'True').lower() == 'true'
        },
        'game': {
            'dictionary_path': os.getenv('DICTIONARY_PATH', 'data/words.txt'),
            'max_guesses': int(os.getenv('MAX_GUESSES', '6')),
            'word_length': int(os.getenv('WORD_LENGTH', '5'))
        },
        'solver': {
            'default': os.getenv('DEFAULT_SOLVER', 'naive'),
            'mcts_simulations': int(os.getenv('MCTS_SIMULATIONS', '1000'))
        },
        'supabase': {
            'url': os.getenv('SUPABASE_URL'),
            'key': os.getenv('SUPABASE_KEY')
        }
    }


# Global configuration instance
config = get_config()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DICTIONARY_PATH = os.path.join(
    BASE_DIR, os.getenv('DICTIONARY_PATH', 'data/words.txt'))

# Game settings
MAX_GUESSES = int(os.getenv('MAX_GUESSES', '6'))
WORD_LENGTH = int(os.getenv('WORD_LENGTH', '5'))

# Web server settings
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '3001'))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Solver settings
DEFAULT_SOLVER = os.getenv('DEFAULT_SOLVER', 'naive')
MCTS_SIMULATIONS = int(os.getenv('MCTS_SIMULATIONS', '100000'))

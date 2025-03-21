"""
Configuration settings for the Wordle solver application.
"""

import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DICTIONARY_PATH = os.path.join(DATA_DIR, 'words.txt')

# Game settings
MAX_GUESSES = 6
WORD_LENGTH = 5

# Web server settings
HOST = '0.0.0.0'
PORT = 3001
DEBUG = True

# Solver settings
DEFAULT_SOLVER = 'naive'
MCTS_SIMULATIONS = 1000  # Number of simulations for MCTS solver

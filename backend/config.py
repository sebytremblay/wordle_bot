import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DICTIONARY_PATH = os.path.join(
    BASE_DIR, os.getenv('DICTIONARY_PATH', 'data/words.txt'))
ORDERED_WORDS_PATH = os.path.join(
    BASE_DIR, os.getenv('ORDERED_WORDS_PATH', 'data/ordered_words.txt'))
WORDLE_ANS_PATH = os.path.join(
    BASE_DIR, os.getenv('WORDLE_ANS_PATH', 'data/wordle_answers.txt'))

# Web server settings
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '3001'))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Supabase settings
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Game settings
MAX_GUESSES = 6
WORD_LENGTH = 5

# Solver settings
DEFAULT_SOLVER = 'greedy'

MCTS_SIMULATIONS = 124
MCTS_REWARD_MULTIPLIER = 0.6393407479710643
MCTS_EXPLORATION_CONSTANT = 0.33125383026412164

MINIMAX_DEPTH = 2

# Random seed
RANDOM_SEED = 42

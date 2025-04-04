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

# Supabase settings
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

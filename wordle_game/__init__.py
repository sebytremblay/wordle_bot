"""
Wordle Solver - A package implementing multiple algorithms for solving Wordle puzzles.
"""

from .wordle_game import WordleGame
from .dictionary import load_dictionary

__version__ = '0.1.0'
__all__ = ['WordleGame', 'load_dictionary']

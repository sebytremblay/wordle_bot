from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class BaseSolver(ABC):
    """Abstract base class for Wordle solvers."""

    def __init__(self, dictionary_words: List[str]):
        """Initialize the solver with a dictionary of valid words.

        Args:
            dictionary_words: List of valid 5-letter words
        """
        self.dictionary = dictionary_words

    @property
    def solver_type(self) -> str:
        """Get the type of this solver."""
        return self.__class__.__name__.lower().replace('solver', '')

    @abstractmethod
    def select_guess(self, candidates: List[str]) -> str:
        """Select the next word to guess based on the current game state.

        Args:
            candidates: List of currently valid candidate words based on game history

        Returns:
            The selected word to guess
        """
        pass

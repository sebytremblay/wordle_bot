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
        self.candidate_words = dictionary_words.copy()

    def initialize(self, candidate_words: Optional[List[str]] = None) -> None:
        """Initialize or reset the solver's candidate word list.

        Args:
            candidate_words: Optional list of words to use as candidates.
                           If None, uses the full dictionary.
        """
        if candidate_words is None:
            self.candidate_words = self.dictionary.copy()
        else:
            self.candidate_words = candidate_words.copy()

    @abstractmethod
    def select_guess(self) -> str:
        """Select the next word to guess.

        Returns:
            The selected word to guess
        """
        pass

    def update(self, guess: str, feedback: Tuple[int, ...]) -> None:
        """Update solver state based on the feedback from a guess.

        Args:
            guess: The word that was guessed
            feedback: Tuple of feedback values (2: green, 1: yellow, 0: gray)
        """
        from ..feedback import filter_candidates
        self.candidate_words = filter_candidates(
            self.candidate_words, guess, feedback)

    def reset(self) -> None:
        """Reset the solver state for a new game."""
        self.initialize()

    def get_candidate_count(self) -> int:
        """Get the number of remaining candidate words.

        Returns:
            Number of words in the candidate set
        """
        return len(self.candidate_words)

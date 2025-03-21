import random
from typing import List
from .base_solver import BaseSolver


class NaiveSolver(BaseSolver):
    """A naive solver that randomly selects from the remaining candidate words."""

    def select_guess(self) -> str:
        """Select a random word from the remaining candidates.

        Returns:
            A randomly selected word from the candidate list
        """
        if not self.candidate_words:
            raise ValueError("No candidate words remaining")

        return random.choice(self.candidate_words)

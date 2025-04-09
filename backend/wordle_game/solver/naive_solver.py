import random
from typing import List
from .base_solver import BaseSolver


class NaiveSolver(BaseSolver):
    """A naive solver that randomly selects from the remaining candidate words."""

    def select_guess(self, candidates: List[str]) -> str:
        """Select a random word from the remaining candidates.

        Args:
            candidates: List of currently valid candidate words

        Returns:
            A randomly selected word from the candidate list
        """
        if not candidates:
            raise ValueError("No candidate words remaining")

        return random.choice(candidates)

    @classmethod
    def get_name(cls) -> str:
        return "naive"

    def starting_word(self) -> str:
        return "crate"

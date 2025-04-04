from abc import ABC, abstractmethod
from typing import List, Tuple, Optional


class BaseSolver(ABC):
    """Abstract base class for Wordle solvers."""

    @abstractmethod
    def select_guess(self, candidates: List[str]) -> str:
        """Select the next word to guess based on the current game state.

        Args:
            candidates: List of currently valid candidate words based on game history

        Returns:
            The selected word to guess
        """
        pass

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """Return a string name representing the solver."""
        pass

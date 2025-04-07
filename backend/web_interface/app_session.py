from typing import Optional, Tuple, List
from wordle_game.wordle_game import WordleGame
from wordle_game.solver_manager import SolverManager
from config import MAX_GUESSES


class AppSession:
    """Manages the state of a single Wordle game session including its solvers."""

    def __init__(self, dictionary_words: List[str], max_guesses: int = MAX_GUESSES, target_word: str = ""):
        """Initialize a new game session.

        Args:
            dictionary_words: List of valid words for the game
            max_guesses: Maximum number of allowed guesses
            target_word: Optional specific target word
        """
        self.game_state = WordleGame(
            dictionary_words=dictionary_words,
            max_guesses=max_guesses,
            target_word=target_word
        )
        self.solver_manager = SolverManager(dictionary_words)

    def submit_guess(self, guess: str) -> Tuple[Tuple[int, ...], bool]:
        """Submit a guess to the game."""
        return self.game_state.submit_guess(guess)

    def get_hint(self, solver_type: Optional[str] = None) -> Tuple[str, str, int]:
        """Get a hint using the specified or active solver.

        Args:
            solver_type: Optional solver type to use. If None, uses active solver.

        Returns:
            Tuple containing:
                - The suggested word
                - The solver type used
                - Number of remaining candidates
        """
        # Get current game state for solver
        candidates = self.game_state.get_remaining_candidates()
        previous_guesses = self.game_state.previous_guesses

        # Get hint from solver manager
        hint, solver_type_used, candidates_remaining = self.solver_manager.get_hint(
            candidates=candidates,
            previous_guesses=previous_guesses,
            solver_type=solver_type
        )

        return hint, solver_type_used, candidates_remaining

    def get_game_state(self) -> dict:
        """Get the current game state."""
        game_state = self.game_state.get_game_state()

        return game_state

    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_state.is_game_over()

    def get_remaining_candidates(self) -> List[str]:
        """Get remaining candidate words."""
        return self.game_state.get_remaining_candidates()

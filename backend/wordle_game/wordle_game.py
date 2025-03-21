from typing import List, Tuple, Optional
import random
from .feedback import compute_feedback, filter_candidates
from .solver_manager import SolverManager


class WordleGame:
    def __init__(self, dictionary_words: List[str], max_guesses: int = 6):
        """Initialize a new Wordle game.

        Args:
            dictionary_words: List of valid 5-letter words
            max_guesses: Maximum number of allowed guesses (default: 6)
        """
        self.dictionary = dictionary_words
        self.max_guesses = max_guesses
        self.target_word: str = ""
        self.candidate_words: List[str] = []
        self.guess_count: int = 0
        self.history: List[Tuple[str, Tuple[int, ...]]] = []
        self.game_won: bool = False
        self.solver_manager = SolverManager(dictionary_words)

    def start_new_game(self) -> None:
        """Start a new game by selecting a random target word."""
        self.target_word = random.choice(self.dictionary)
        self.candidate_words = self.dictionary.copy()
        self.guess_count = 0
        self.history = []
        self.game_won = False
        self.solver_manager = SolverManager(self.dictionary)

    def submit_guess(self, guess: str) -> Tuple[Tuple[int, ...], bool]:
        """Submit a guess and get feedback.

        Args:
            guess: A 5-letter word guess

        Returns:
            Tuple containing:
                - Feedback tuple (2: green, 1: yellow, 0: gray)
                - Boolean indicating if the game is over
        """
        if not self._is_valid_guess(guess):
            raise ValueError("Invalid guess")

        if self.is_game_over():
            raise ValueError("Game is already over")

        feedback = compute_feedback(guess, self.target_word)
        self.history.append((guess, feedback))
        self.guess_count += 1

        # Update candidate words based on feedback
        self.candidate_words = filter_candidates(
            self.candidate_words, guess, feedback)

        # Update all solvers with the new feedback
        self.solver_manager.update_all(guess, feedback)

        # Check if game is won
        self.game_won = (guess == self.target_word)

        return feedback, self.is_game_over()

    def is_game_over(self) -> bool:
        """Check if the game is over (won or max guesses reached)."""
        return self.game_won or self.guess_count >= self.max_guesses

    def get_game_state(self) -> dict:
        """Get the current game state.

        Returns:
            Dictionary containing game state information
        """
        active_solver = self.solver_manager.get_active_solver()
        return {
            "guesses_made": self.guess_count,
            "max_guesses": self.max_guesses,
            "remaining_guesses": self.max_guesses - self.guess_count,
            "history": self.history,
            "game_over": self.is_game_over(),
            "game_won": self.game_won,
            "candidates_remaining": len(self.candidate_words),
            "active_solver": active_solver.solver_type if active_solver else None
        }

    def _is_valid_guess(self, guess: str) -> bool:
        """Check if a guess is valid (5 letters and in dictionary)."""
        return len(guess) == 5 and guess.lower() in self.dictionary

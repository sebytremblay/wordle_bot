from typing import List, Tuple, Optional
import random
from .feedback import compute_feedback, filter_candidates
from .solver_manager import SolverManager


class WordleGame:
    def __init__(self, dictionary_words: List[str], max_guesses: int = 6, target_word: str = "", is_wordle_list: bool = False):
        """Initialize a new Wordle game.

        Args:
            dictionary_words: List of valid n-letter words
            max_guesses: Maximum number of allowed guesses (default: 6)
        """
        self.dictionary = dictionary_words
        self.max_guesses = max_guesses

        # Randomly generate target word if not provided
        if target_word == "":
            self.target_word = random.choice(self.dictionary)
        else:
            self.target_word = target_word

        self.candidate_words: List[str] = self.dictionary.copy()
        self.guess_count: int = 0
        self.history: List[Tuple[str, Tuple[int, ...]]] = []
        self.game_won: bool = False
        self.solver_manager = SolverManager(dictionary_words, is_wordle_list)
        
        # Track previous guesses to prevent repetition
        self.previous_guesses: set[str] = set()

    def submit_guess(self, guess: str) -> Tuple[Tuple[int, ...], bool]:
        """Submit a guess and get feedback.

        Args:
            guess: A n-letter word guess

        Returns:
            Tuple containing:
                - Feedback tuple (2: green, 1: yellow, 0: gray)
                - Boolean indicating if the game is over
        """
        if not self._is_valid_guess(guess):
            raise ValueError(f"Invalid guess: {guess}")

        if self.is_game_over():
            raise ValueError("Game is already over")

        feedback = compute_feedback(guess, self.target_word)
        self.history.append((guess, feedback))
        self.guess_count += 1
        
        # Add to previous guesses set
        self.previous_guesses.add(guess)

        # Update candidate words based on feedback
        self.candidate_words = filter_candidates(
            self.candidate_words, guess, feedback)
            

        # Check if game is won
        self.game_won = (guess == self.target_word)

        return feedback, self.is_game_over()

    def get_hint(self, solver_type: Optional[str] = None) -> Tuple[str, str, int]:
        """Get a hint from the specified solver type.

        Args:
            solver_type: Optional solver type to use. If None, uses active solver.

        Returns:
            Tuple containing:
                - The suggested word
                - The solver type used
                - Number of remaining candidates
        """
        if solver_type:
            solver = self.solver_manager.get_solver(solver_type)
        else:
            solver = self.solver_manager.get_active_solver()
            if not solver:
                solver = self.solver_manager.get_solver('naive')

        # Get suggested guess from solver
        hint = solver.select_guess(self.candidate_words)
        
        # If the hint is a word we've already guessed, find a different word
        if hint in self.previous_guesses:
            # Find the first unguessed word from candidates
            for word in self.candidate_words:
                if word not in self.previous_guesses:
                    hint = word
                    break
            
            # If all candidates have been guessed, pick any unguessed word from dictionary
            if hint in self.previous_guesses:
                for word in self.dictionary:
                    if word not in self.previous_guesses:
                        hint = word
                        break
        
        return hint, solver.solver_type(), len(self.candidate_words)

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
            "active_solver": active_solver.solver_type() if active_solver else None,
            "previous_guesses": list(self.previous_guesses)
        }

    def _is_valid_guess(self, guess: str) -> bool:
        """Check if a guess is valid."""
        return guess in self.dictionary

    def get_remaining_candidates(self) -> List[str]:
        """Get the list of remaining candidate words."""
        return self.candidate_words

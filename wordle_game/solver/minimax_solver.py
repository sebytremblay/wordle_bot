from typing import List, Dict, Tuple, Optional
from collections import defaultdict
from .base_solver import BaseSolver
from ..feedback import compute_feedback


class MinimaxSolver(BaseSolver):
    """A solver that uses minimax with alpha-beta pruning to minimize worst-case scenarios."""

    def __init__(self, dictionary_words: List[str], max_depth: int = 3):
        """Initialize the solver.

        Args:
            dictionary_words: List of valid 5-letter words
            max_depth: Maximum depth for minimax search (default: 3)
        """
        super().__init__(dictionary_words)
        self.max_depth = max_depth

    def select_guess(self) -> str:
        """Select a guess using minimax search with alpha-beta pruning.

        The strategy:
        1. For each possible guess, simulate all possible feedback patterns
        2. Use minimax to find the guess that minimizes the maximum remaining candidates
        3. Use alpha-beta pruning to optimize the search

        Returns:
            The word that minimizes the worst-case scenario
        """
        if len(self.candidate_words) <= 2:
            return self.candidate_words[0]

        best_score = float('inf')
        best_guess = None
        alpha = float('-inf')
        beta = float('inf')

        # Consider all remaining candidates as possible guesses
        for guess in self.candidate_words:
            score = self._minimax(guess, self.max_depth, alpha, beta)
            if score < best_score:  # We want to minimize the worst case
                best_score = score
                best_guess = guess
            beta = min(beta, score)

        return best_guess if best_guess else self.candidate_words[0]

    def _minimax(self, guess: str, depth: int, alpha: float, beta: float) -> float:
        """Recursive minimax function with alpha-beta pruning.

        Args:
            guess: The word to evaluate
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning

        Returns:
            Score representing the worst-case number of remaining candidates
        """
        if depth == 0 or len(self.candidate_words) <= 1:
            return len(self.candidate_words)

        # Get partitions for this guess
        partitions = self._compute_partitions(guess)

        # Find the worst case (maximum remaining candidates)
        worst_case = float('-inf')

        for feedback_pattern, words in partitions.items():
            # Save current state
            saved_candidates = self.candidate_words

            # Update state for this branch
            self.candidate_words = words

            # Recursively evaluate this partition
            score = self._minimax_step(depth - 1, alpha, beta)
            worst_case = max(worst_case, score)

            # Restore state
            self.candidate_words = saved_candidates

            # Alpha-beta pruning
            if worst_case >= beta:
                return worst_case
            alpha = max(alpha, worst_case)

        return worst_case

    def _minimax_step(self, depth: int, alpha: float, beta: float) -> float:
        """Helper function for minimax recursion.

        Args:
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning

        Returns:
            Score for this branch
        """
        if len(self.candidate_words) <= 2:
            return len(self.candidate_words)

        best_score = float('inf')

        # Only consider a subset of candidates for deeper levels to improve performance
        candidates_to_check = self.candidate_words[:min(
            len(self.candidate_words), 10)]

        for guess in candidates_to_check:
            score = self._minimax(guess, depth, alpha, beta)
            best_score = min(best_score, score)

            # Alpha-beta pruning
            if best_score <= alpha:
                return best_score
            beta = min(beta, best_score)

        return best_score

    def _compute_partitions(self, guess: str) -> Dict[Tuple[int, ...], List[str]]:
        """Compute how a guess would partition the remaining candidates.

        Args:
            guess: The word to evaluate

        Returns:
            Dictionary mapping feedback patterns to lists of matching words
        """
        partitions = defaultdict(list)

        for word in self.candidate_words:
            feedback = compute_feedback(guess, word)
            partitions[feedback].append(word)

        return dict(partitions)

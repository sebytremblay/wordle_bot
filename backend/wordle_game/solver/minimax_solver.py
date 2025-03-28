from typing import List, Dict, Tuple
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
        self.dictionary_words = dictionary_words
        self.max_depth = max_depth

    def select_guess(self, candidates: List[str]) -> str:
        """Select a guess using minimax search with alpha-beta pruning.

        Args:
            candidates: List of currently valid candidate words

        The strategy:
        1. For each possible guess, simulate all possible feedback patterns
        2. Use minimax to find the guess that minimizes the maximum remaining candidates
        3. Use alpha-beta pruning to optimize the search

        Returns:
            The word that minimizes the worst-case scenario
        """
        if len(candidates) <= 2:
            return candidates[0]

        best_score = float('inf')
        best_guess = None
        alpha = float('-inf')
        beta = float('inf')

        # Consider all remaining candidates as possible guesses
        for guess in candidates:
            score = self._minimax(guess, self.max_depth,
                                  alpha, beta, candidates)
            if score < best_score:  # We want to minimize the worst case
                best_score = score
                best_guess = guess
            beta = min(beta, score)

        return best_guess if best_guess else candidates[0]

    def _minimax(self, guess: str, depth: int, alpha: float, beta: float, candidates: List[str]) -> float:
        """Recursive minimax function with alpha-beta pruning.

        Args:
            guess: The word to evaluate
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            candidates: List of currently valid candidate words

        Returns:
            Score representing the worst-case number of remaining candidates
        """
        if depth == 0 or len(candidates) <= 1:
            return len(candidates)

        # Get partitions for this guess
        partitions = self._compute_partitions(guess, candidates)

        # Find the worst case (maximum remaining candidates)
        worst_case = float('-inf')

        for feedback_pattern, words in partitions.items():
            # Recursively evaluate this partition
            score = self._minimax_step(depth - 1, alpha, beta, words)
            worst_case = max(worst_case, score)

            # Alpha-beta pruning
            if worst_case >= beta:
                return worst_case
            alpha = max(alpha, worst_case)

        return worst_case

    def _minimax_step(self, depth: int, alpha: float, beta: float, candidates: List[str]) -> float:
        """Helper function for minimax recursion.

        Args:
            depth: Current depth in the search tree
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            candidates: List of currently valid candidate words

        Returns:
            Score for this branch
        """
        if len(candidates) <= 2:
            return len(candidates)

        best_score = float('inf')

        # Only consider a subset of candidates for deeper levels to improve performance
        candidates_to_check = candidates[:min(len(candidates), 10)]

        for guess in candidates_to_check:
            score = self._minimax(guess, depth, alpha, beta, candidates)
            best_score = min(best_score, score)

            # Alpha-beta pruning
            if best_score <= alpha:
                return best_score
            beta = min(beta, best_score)

        return best_score

    def _compute_partitions(self, guess: str, candidates: List[str]) -> Dict[Tuple[int, ...], List[str]]:
        """Compute how a guess would partition the remaining candidates.

        Args:
            guess: The word to evaluate
            candidates: List of currently valid candidate words

        Returns:
            Dictionary mapping feedback patterns to lists of matching words
        """
        partitions = defaultdict(list)

        for word in candidates:
            feedback = compute_feedback(guess, word)
            partitions[feedback].append(word)

        return dict(partitions)

from typing import List, Dict, Tuple
import math
from collections import defaultdict
from .base_solver import BaseSolver
from ..feedback import compute_feedback


class GreedySolver(BaseSolver):
    """A solver that uses information gain to select guesses."""

    def select_guess(self, candidates: List[str]) -> str:
        """Select a guess that maximizes expected information gain.

        Args:
            candidates: List of currently valid candidate words

        The strategy:
        1. For each possible guess, compute how it would partition the remaining candidates
        2. Calculate the expected information gain from each partition
        3. Choose the guess that gives the highest expected information gain

        Returns:
            The word with highest expected information gain
        """
        if len(candidates) <= 2:
            return candidates[0]

        best_score = float('-inf')
        best_guess = None

        # Consider all remaining candidates as possible guesses
        for guess in candidates:
            score = self._compute_expected_info_gain(guess, candidates)
            if score > best_score:
                best_score = score
                best_guess = guess

        return best_guess if best_guess else candidates[0]

    def _compute_expected_info_gain(self, guess: str, candidates: List[str]) -> float:
        """Compute the expected information gain for a guess.

        Args:
            guess: The word to evaluate
            candidates: List of currently valid candidate words

        Returns:
            Expected information gain (in bits)
        """
        # Get the current entropy (before guess)
        initial_entropy = math.log2(len(candidates))

        # Compute partitions for this guess
        partitions = self._compute_partitions(guess, candidates)

        # Compute expected entropy after guess
        total_words = len(candidates)
        expected_entropy = 0.0

        for feedback_pattern, words in partitions.items():
            prob = len(words) / total_words
            if prob > 0:
                expected_entropy += prob * math.log2(len(words))

        # Information gain is reduction in entropy
        return initial_entropy - expected_entropy

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

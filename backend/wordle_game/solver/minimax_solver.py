from typing import List, Dict, Tuple
from collections import defaultdict
from .base_solver import BaseSolver
from ..feedback import compute_feedback


class MinimaxSolver(BaseSolver):
    """A solver that uses minimax with alpha-beta pruning to minimize worst-case scenarios."""

    def __init__(self, ordered_words: List[str]):
        """Initialize the solver.

        Args:
            ordered_words: List of valid 5-letter words (ordered by heuristic to improve alpha beta pruning)
        """
        self.ordered_words = ordered_words
        # For performance: Use ordered_words as a guide for which guesses to try first

    def select_guess(self, candidates: List[str]) -> str:
        """Select a guess using minimax search with alpha-beta pruning.

        Args:
            candidates: List of currently valid candidate words

        Returns:
            The word that minimizes the worst-case scenario
        """
        # handle base case -- too many candidates to process efficiently
        if len(candidates) > 10000:
            # takes too long if there are too many words, so just pick based on info gain according to heuristic
            return self.ordered_words[0]
            
        # If only a few candidates remain, prioritize candidates first as guesses
        if len(candidates) <= 2:
            return candidates[0]
            
        # Get the guesses to try (prioritize words from ordered_words that are also in candidates)
        guess_words = []
        # First try words that are also potential answers
        for word in self.ordered_words:
            if word in candidates:
                guess_words.append(word)
            if len(guess_words) >= 100:  # Limit to first 100 for performance
                break
                
        # If no valid guesses from ordered words in candidates, use candidates directly
        if not guess_words:
            guess_words = candidates[:100]  # Limit to first 100 for performance
        
        return self._minimax(guess_words, candidates)

    def _minimax(self, guess_words: List[str], candidates: List[str], prune=True, alpha=float('-inf'), beta=float('inf')):
        """Find the best guess using minimax algorithm.
        
        Args:
            guess_words: List of words to consider as guesses
            candidates: List of possible answers
            
        Returns:
            The best guess word
        """
        if not candidates:
            raise ValueError("Remaining words list is empty.")
            
        # Select the guess that minimizes the maximum number of remaining words in the worst-case scenario
        best_score = float('inf')  # Lower score is better -> fewer words remaining
        best_guess = guess_words[0] if guess_words else candidates[0]
        
        for guess in guess_words:
            outcomes = self._get_outcomes(guess, candidates)
            worst_case = max(len(words) for words in outcomes.values())
            
            # If this guess has a better worst-case than previous guesses
            if worst_case < best_score:
                best_score = worst_case
                best_guess = guess
                if prune:
                    alpha = max(alpha, best_score)
                    
            if prune and beta <= alpha:
                break  # prune this branch
                
        return best_guess
    
    def _get_outcomes(self, guess: str, remaining_words: List[str]) -> Dict[Tuple[int, ...], List[str]]:
        """Get all possible outcomes for a given guess.
        
        Args:
            guess: The word to guess
            remaining_words: All possible target words
            
        Returns:
            Dictionary mapping feedback patterns to lists of remaining words
        """
        outcomes = defaultdict(list)
        
        # For each possible target word, compute the feedback and group by feedback pattern
        for word in remaining_words:
            feedback = compute_feedback(guess, word)
            outcomes[feedback].append(word)
            
        return outcomes

    @staticmethod
    def _estimate_feedback_spread(words):
        """Ranks words with a heuristic to maximize pruning based on feedback spread.
        
        Args:
            words: List of words to rank
            
        Returns:
            Sorted list of words by estimated information gain
        """
        estimated_scores = {
            word: sum(len(set(word) & set(other)) for other in words) / len(words)
            for word in words
        }
        return sorted(words, key=lambda w: (-estimated_scores[w], -len(set(w))))
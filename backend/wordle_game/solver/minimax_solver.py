from typing import List, Dict, Tuple
from collections import defaultdict
from .base_solver import BaseSolver
from ..feedback import compute_feedback
from wordle_game.dictionary import load_dictionary
import config


class Node:
    def __init__(self, guess: str, remaining_words: List[str]):
        self.guess = guess
        self.remaining_words = remaining_words
        # child nodes grouped by feedback patterns
        self.outcomes = defaultdict(list)
        self.best_score = float('inf')  # score for pruning

    def add_outcome(self, feedback: Tuple[int, ...], word: str):
        self.outcomes[feedback].append(word)

    def evaluate(self):
        """Evaluate the worst-case outcome for this node (minimax score)"""
        if not self.outcomes:
            return 0  # no outcomes, no remaining words

        worst_case = max(len(words) for words in self.outcomes.values())
        self.best_score = worst_case
        return worst_case


class MinimaxSolver(BaseSolver):
    """A solver that uses minimax with alpha-beta pruning to minimize worst-case scenarios."""

    def __init__(self, words: List[str], ordered_words: List[str]):
        """Initialize the solver.

        Args:
            words: List of valid words
            ordered_words: List of valid 5-letter words (ordered by heuristic to improve alpha beta pruning)
        """
        self.ordered_words = [word for word in ordered_words if word in words]
        self.max_depth = config.MINIMAX_DEPTH
        # cache to avoid redundant computation
        self.cache = {}

    def select_guess(self, candidates: List[str]) -> str:
        """Select a guess using minimax search with alpha-beta pruning.

        Args:
            candidates: List of currently valid candidate words

        Returns:
            The word that minimizes the worst-case scenario
        """
        # handle base case -- (assuming ordered words is in order of estimates info gain)
        # too many candidates to process efficiently, pick best word using heuristic
        if len(candidates) > 10000:
            return self.ordered_words[0]

        if len(candidates) <= 2:
            return candidates[0]

        # clear cache for new search
        self.cache = {}

        # Find best guess using minimax search
        best_guess, _ = self._minimax(candidates, 0)
        return best_guess

    def _minimax(self, candidates: List[str], depth: int) -> Tuple[str, int]:
        """Find the best guess and its score using minimax algorithm with specified depth.

        Args:
            candidates: List of possible target words
            depth: Current depth in the search tree

        Returns:
            Tuple of (best guess word, worst-case score)
        """
        cache_key = (tuple(sorted(candidates)), depth)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # base cases: max depth reached or few candidates remain
        if depth >= self.max_depth or len(candidates) <= 2:
            best_guess = candidates[0] if len(
                candidates) <= 2 else self._evaluate_guesses(candidates)
            best_score = 1 if len(candidates) <= 1 else len(candidates)
            self.cache[cache_key] = (best_guess, best_score)
            return best_guess, best_score

        best_guess = None
        best_score = float('inf')
        i = 0
        for guess in candidates[:15]:
            #   for optimization, only consider 15 best words based on ordering heuristic
            #   I found that the best word found is always within the first 10 remaining words
            #   because it is ordered by the heuristic, the subset of 15 did not jeapordize accuracy
            outcomes = self._get_outcomes(guess, candidates)

            # perfectly splits candidates - optimal
            if all(len(words) <= 1 for words in outcomes.values()):
                self.cache[cache_key] = (guess, 1)
                return guess, 1

            worst_case_score = 0
            should_prune = False

            for _, remaining_words in outcomes.items():
                if not remaining_words:
                    continue

                if len(remaining_words) == 1:  # branch is solved
                    outcome_score = 1
                # max depth or few words
                elif depth + 1 >= self.max_depth or len(remaining_words) <= 2:
                    outcome_score = len(remaining_words)
                else:
                    # recursively find the best guess for this subset
                    _, outcome_score = self._minimax(
                        remaining_words, depth + 1)

                worst_case_score = max(worst_case_score, outcome_score)

                if worst_case_score >= best_score:  # prune
                    should_prune = True
                    break

            if should_prune:
                continue

            if worst_case_score < best_score:
                best_score = worst_case_score
                best_guess = guess

                # perfect guess
                if best_score == 1:
                    break
            i += 1

        self.cache[cache_key] = (best_guess, best_score)
        # print(i)
        return best_guess, best_score

    def _evaluate_guesses(self, candidates: List[str]) -> str:
        """Evaluate all guesses and return the one with the lowest worst-case score."""
        best_guess = None
        best_score = float('inf')

        for guess in candidates:
            outcomes = self._get_outcomes(guess, candidates)
            worst_case = max(len(words)
                             for words in outcomes.values()) if outcomes else 0

            if worst_case < best_score:
                best_score = worst_case
                best_guess = guess

                # perfect guess
                if best_score == 1:
                    break

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

        # for each possible target word, compute the feedback and group by feedback pattern
        for word in remaining_words:
            feedback = compute_feedback(guess, word)
            outcomes[feedback].append(word)

        return outcomes

    @classmethod
    def get_name(cls) -> str:
        return f"minimax_{config.MINIMAX_DEPTH}"

    @staticmethod
    def _estimate_feedback_spread(words):
        """Ranks words with a heuristic to maximize pruning based on feedback spread.

        Args:
            words: List of words to rank

        Returns:
            Sorted list of words by estimated information gain
        """
        estimated_scores = {
            word: sum(len(set(word) & set(other))
                      for other in words) / len(words)
            for word in words
        }
        return sorted(words, key=lambda w: (-estimated_scores[w], -len(set(w))))

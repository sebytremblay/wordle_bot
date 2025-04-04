from typing import List, Dict, Optional, Tuple
import random
import math

from ..wordle_game import WordleGame
from .base_solver import BaseSolver
from ..feedback import compute_feedback
import config


class MCTSNode:
    """Node in the Monte Carlo Tree Search with candidate set state."""

    def __init__(self, candidate_set: List[str], guess: Optional[str] = None, parent: Optional['MCTSNode'] = None):
        self.candidate_set = candidate_set  # Current valid words given past feedback
        self.guess = guess
        self.parent = parent
        self.children: Dict[Tuple[int, ...], 'MCTSNode'] = {}
        self.visits = 0
        self.value = 0.0
        self.untried_moves: List[str] = candidate_set.copy()

    def add_child(self, feedback: Tuple[int, ...], guess: str) -> 'MCTSNode':
        """Add a child node with updated candidate set based on feedback."""
        # Filter the candidate set using the feedback from the guess
        new_candidates = [word for word in self.candidate_set if compute_feedback(
            guess, word) == feedback]
        node = MCTSNode(candidate_set=new_candidates, guess=guess, parent=self)
        self.children[feedback] = node
        return node

    def update(self, result: float):
        """Update node statistics."""
        self.visits += 1
        self.value += result

    def get_ucb(self, exploration: float = math.sqrt(2)) -> float:
        """Get the UCB1 value for this node."""
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + exploration * math.sqrt(math.log(self.parent.visits) / self.visits)


class MCTSSolver(BaseSolver):
    """A solver that uses Monte Carlo Tree Search for probabilistic optimization."""

    def __init__(self, dictionary_words: List[str], simulations: int = config.MCTS_SIMULATIONS):
        """Initialize the solver.

        Args:
            dictionary_words: List of valid 5-letter words
            simulations: Number of MCTS simulations to run
        """
        self.dictionary = dictionary_words
        self.simulations = simulations

    def select_guess(self, candidates: List[str]) -> str:
        """Select a guess using Monte Carlo Tree Search.

        Args:
            candidates: List of currently valid candidate words

        The strategy:
        1. Build a search tree through repeated simulations
        2. At each node:
            - Selection: Choose promising nodes using UCB1
            - Expansion: Add new nodes to explore
            - Simulation: Play out random games
            - Backpropagation: Update node statistics
        3. Choose the most visited root child

        Returns:
            The most promising word according to MCTS
        """
        if len(candidates) == 1:
            return candidates[0]

        # Initialize root node with full candidate set
        root = MCTSNode(candidate_set=candidates.copy())

        # Run simulations
        for _ in range(self.simulations):
            node = root
            curr_guesses = 0
            # Select a target from the current state consistently
            target_word = random.choice(node.candidate_set)

            # Selection
            while not node.untried_moves and node.children:
                node = self._select_ucb(node)
                curr_guesses += 1

            # Expansion
            if node.untried_moves:
                guess = self._rollout(node.untried_moves)
                if guess in node.untried_moves:
                    node.untried_moves.remove(guess)
                feedback = compute_feedback(guess, target_word)
                node = node.add_child(feedback, guess)

            # Simulation using the node's candidate set
            reward = self._simulate(
                node.candidate_set, target_word, curr_guesses)

            # Backpropagation
            while node is not None:
                node.update(reward)
                node = node.parent

        # Choose best move (most visited child) and return its guess
        best_child = max(root.children.values(),
                         key=lambda child: child.visits)
        return best_child.guess if best_child.guess is not None else candidates[0]

    def _select_ucb(self, node: MCTSNode) -> MCTSNode:
        """Select a child node using UCB1."""
        return max(node.children.values(), key=lambda child: child.get_ucb())

    def _simulate(self, candidates: List[str], target_word: str, curr_guesses: int = 0) -> float:
        """Run a random simulation from the current node.

        Args:
            candidates: List of currently valid candidate words
            target_word: The word to be guessed
            curr_guesses: Number of guesses made so far

        Returns:
            Score between 0 and 1
        """
        if not candidates:
            return 0.0

        # Prepare a simulation from this current state
        remaining_guesses = config.MAX_GUESSES - curr_guesses
        simulation = WordleGame(
            self.dictionary, remaining_guesses, target_word)
        simulation.candidate_words = candidates

        # Run the simulation
        while not simulation.is_game_over():
            guess = self._rollout(simulation.candidate_words)
            simulation.submit_guess(guess)

        # Return the reward
        reward = (1 - simulation.guess_count /
                  simulation.max_guesses) if simulation.game_won else 0
        return reward

    def _rollout(self, candidates: List[str]) -> str:
        """Determine the best word to guess using information theory approximation.

        1. Computes letter frequencies of remaining candidates
        2. Assigns scores to each word based on unique letter coverage and position

        Args:
            candidates: List of currently valid candidate words

        Returns:
            The selected word for this rollout
        """
        # Fast letter frequency calculation
        letter_freqs = {}
        position_freqs = [{} for _ in range(5)]

        # Count letter and position frequencies
        for word in candidates:
            for i, char in enumerate(word):
                letter_freqs[char] = letter_freqs.get(char, 0) + 1
                position_freqs[i][char] = position_freqs[i].get(char, 0) + 1

        # Initialize best word and score
        total_words = len(candidates)
        best_score = -1
        best_word = candidates[0]

        # Score each word based on its information value
        for word in self.dictionary:
            # Skip words with repeated letters for early guesses (more efficient information gain)
            if len(set(word)) < 4 and len(candidates) > 10:
                continue

            # Calculate word score based on letter frequencies and uniqueness
            score = 0
            seen_letters = set()

            for i, char in enumerate(word):
                # Skip if we've already counted this letter in this word
                if char in seen_letters:
                    continue
                seen_letters.add(char)

                # Letter frequency score
                char_freq = letter_freqs.get(
                    char, 0) / total_words if total_words > 0 else 0

                # Prefer letters that appear in ~50% of words
                letter_info_value = 1.0 - abs(0.5 - char_freq) * 2.0

                # Position frequency score to prioritize letters that appear in the same position in most words
                pos_freq = position_freqs[i].get(
                    char, 0) / total_words if total_words > 0 else 0
                position_info_value = 1.0 - abs(0.5 - pos_freq) * 2.0

                # Combine scores with position information weighted less
                score += letter_info_value * 0.7 + position_info_value * 0.3

            # Normalize by number of unique letters
            score = score / max(1, len(seen_letters))

            # If this word is in candidates, give it a bonus
            if word in candidates:
                score *= 1.2

            # Update best word if we found a better score
            if score > best_score:
                best_score = score
                best_word = word

        # If we didn't find a good word in our dictionary subset, fall back to a candidate
        if best_word not in self.dictionary or best_score < 0:
            return random.choice(candidates)

        return best_word

    @classmethod
    def get_name(cls) -> str:
        return f"mcts_{config.MCTS_SIMULATIONS}"

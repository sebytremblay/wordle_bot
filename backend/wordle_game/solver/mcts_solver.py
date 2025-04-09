from typing import List, Dict, Optional, Tuple
import random
import math

from ..wordle_game import WordleGame
from .base_solver import BaseSolver
from ..feedback import compute_feedback, filter_candidates
import config


class MCTSNode:
    """Node in the Monte Carlo Tree Search with candidate set state."""

    def __init__(self, candidate_set: List[str], guess: Optional[str] = None, parent: Optional['MCTSNode'] = None):
        self.candidate_set = candidate_set  # Current valid words given past feedback
        self.guess = guess
        self.parent = parent
        # Use a composite key (guess, feedback) to avoid collisions when feedbacks match
        self.children: Dict[Tuple[str, Tuple[int, ...]], 'MCTSNode'] = {}
        self.visits = 0
        self.value = 0.0
        self.untried_moves: List[str] = candidate_set.copy()
        self.made_guess = False

    def add_child(self, feedback: Tuple[int, ...], guess: str) -> 'MCTSNode':
        """Add a child node with updated candidate set based on feedback.

        Args:
            feedback: Tuple of ints representing the feedback for the guess
            guess: The guess that was made

        Returns:
            The child node that was added
        """
        new_candidates = list(filter_candidates(
            tuple(self.candidate_set), guess, feedback))
        node = MCTSNode(candidate_set=new_candidates, guess=guess, parent=self)
        self.children[(guess, feedback)] = node
        return node

    def update(self, result: float):
        """Update node statistics.

        Args:
            result: The result of the simulation
        """
        self.visits += 1
        self.value += result

    def get_ucb(self, exploration: float = math.sqrt(2)) -> float:
        """Get the UCB1 value for this node.

        Args:
            exploration: The exploration parameter

        Returns:
            The UCB1 value for this node
        """
        if self.visits == 0:
            return float('inf')
        return (self.value / self.visits) + exploration * math.sqrt(math.log(self.parent.visits) / self.visits)


class MCTSSolver(BaseSolver):
    """A solver that uses Monte Carlo Tree Search for probabilistic optimization."""

    def __init__(self, dictionary_words: List[str], ordered_words: List[str], simulations: int = config.MCTS_SIMULATIONS):
        """Initialize the solver.

        Args:
            dictionary_words: List of valid 5-letter words
            simulations: Number of MCTS simulations to run
        """
        self.dictionary = dictionary_words
        self.simulations = simulations
        self.ordered_words = ordered_words

    def select_guess(self, candidates: List[str]) -> str:
        """Select a guess using Monte Carlo Tree Search.

        Args:
            candidates: List of currently valid words

        Returns:
            The most promising word according to MCTS
        """
        if len(candidates) == 1:
            return candidates[0]
        if not self.made_guess:
            self.made_guess = True
            return "crate"

        # Initialize root node with full candidate set
        root = MCTSNode(candidate_set=candidates.copy())

        # Run simulations
        for _ in range(self.simulations):
            node = root
            curr_guesses = 0
            target_word = random.choice(self.ordered_words[:15])

            # Selection
            while not node.untried_moves and node.children:
                node = self._select_ucb(node)
                curr_guesses += 1

            # Expansion
            if node.untried_moves:
                guess = self._rollout(node.untried_moves)
                if guess is None:
                    continue  # Skip expansion if no valid guess exists

                node.untried_moves.remove(guess)
                curr_guesses += 1
                feedback = compute_feedback(guess, target_word)
                node = node.add_child(feedback, guess)

            # Simulation
            reward = self._simulate(
                node.candidate_set, target_word, curr_guesses)

            # Backpropagation
            while node is not None:
                node.update(reward)
                node = node.parent

        # Choose best move
        best_child = max(root.children.values(),
                         key=lambda child: child.visits)
        return best_child.guess if best_child.guess is not None else candidates[0]

    def _select_ucb(self, node: MCTSNode) -> MCTSNode:
        """Select a child node using UCB1.

        Args:
            node: The node to select a child from

        Returns:
            The child node with the highest UCB1 value
        """
        return max(node.children.values(), key=lambda child: child.get_ucb())

    def _simulate(self, candidates: List[str], target_word: str, curr_guesses: int = 0) -> float:
        """Run a random simulation from the current node.

        Args:
            candidates: List of currently valid words
            target_word: The target word to simulate
            curr_guesses: The number of guesses made so far

        Returns:
            The reward for the simulation
        """
        if not candidates:
            return 0.0
        reward_multiplier = 1

        # Adjust remaining guesses to account for moves already made
        remaining_guesses = config.MAX_GUESSES - curr_guesses
        simulation = WordleGame(
            self.dictionary, remaining_guesses, target_word)
        simulation.candidate_words = list(candidates)

        # Run the simulation
        while not simulation.is_game_over():
            guess = self._rollout(simulation.candidate_words)
            if guess is None:
                return -1 * reward_multiplier

            simulation.submit_guess(guess)

        # Compute the reward based on remaining guesses if the game is won
        reward = (1 - simulation.guess_count /
                  simulation.max_guesses) if simulation.game_won else 0
        return reward * reward_multiplier

    def _rollout(self, candidates: List[str]) -> Optional[str]:
        """Return the best guess from the remaining candidates in the sorted word list.

        Args:
            candidates: List of currently valid words

        Returns:
            The best guess from the remaining candidates
        """
        # Return most optimal word in heuristic ordering
        for word in self.ordered_words:
            if word in candidates:
                return word

        return None

    @classmethod
    def get_name(cls) -> str:
        return f"mcts_{config.MCTS_SIMULATIONS}"

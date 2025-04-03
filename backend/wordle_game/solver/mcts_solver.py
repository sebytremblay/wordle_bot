from typing import List, Dict, Optional
import random
import math

from ..wordle_game import WordleGame
from .base_solver import BaseSolver
import config


class MCTSNode:
    """Node in the Monte Carlo Tree Search."""

    def __init__(self, guess: Optional[str] = None, parent: Optional['MCTSNode'] = None):
        self.guess = guess
        self.parent = parent
        self.children: Dict[str, 'MCTSNode'] = {}  # guess -> node
        self.visits = 0
        self.value = 0.0
        self.untried_moves: List[str] = []

    def add_child(self, guess: str) -> 'MCTSNode':
        """Add a child node with the given guess and feedback."""
        node = MCTSNode(guess=guess, parent=self)
        self.children[guess] = node
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
        if len(candidates) <= 2:
            return candidates[0]

        # Initialize root node
        root = MCTSNode()
        root.untried_moves = candidates.copy()

        # Run simulations
        for _ in range(self.simulations):
            node = root
            curr_guesses = 0

            # Selection
            while node.untried_moves == [] and node.children:
                node = self._select_ucb(node)
                curr_guesses += 1

            # Expansion
            if node.untried_moves:
                guess = self._rollout(node.untried_moves)
                node.untried_moves.remove(guess)
                node = node.add_child(guess)

            # Simulation
            reward = self._simulate(candidates, curr_guesses)

            # Backpropagation
            while node is not None:
                node.update(reward)
                node = node.parent

        # Choose best move (most visited child)
        best_guess = max(root.children.items(),
                         key=lambda child: child[1].visits)[0]
        return best_guess if best_guess else candidates[0]

    def _select_ucb(self, node: MCTSNode) -> MCTSNode:
        """Select a child node using UCB1."""
        return max(node.children.values(), key=lambda child: child.get_ucb())

    def _simulate(self, candidates: List[str], curr_guesses: int = 0) -> float:
        """Run a random simulation from the current node.

        Args:
            candidates: List of currently valid candidate words
            curr_guesses: Number of guesses made so far

        Returns:
            Score between 0 and 1
        """
        if not candidates:
            return 0.0

        # Prepare a simulation from this current state, setting the
        # target word as a random sampling of the remaining guesses
        remaining_guesses = config.MAX_GUESSES - curr_guesses
        simulation = WordleGame(candidates, remaining_guesses, target_word="")

        # Run the simulation
        while not simulation.is_game_over():
            guess = self._rollout(simulation.candidate_words)
            simulation.submit_guess(guess)

        # Return the reward
        reward = (1 - simulation.guess_count /
                  simulation.max_guesses) if simulation.game_won else 0
        return reward

    def _rollout(self, candidates: List[str]) -> float:
        """Determine the best word to guess from the current state."""
        return random.choice(candidates)

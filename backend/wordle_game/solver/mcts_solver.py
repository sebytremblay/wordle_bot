import os
from typing import List, Dict, Tuple, Optional
import random
import math
from collections import defaultdict
from .base_solver import BaseSolver
from ..feedback import compute_feedback


class MCTSNode:
    """Node in the Monte Carlo Tree Search."""

    def __init__(self, guess: Optional[str] = None, parent: Optional['MCTSNode'] = None):
        self.guess = guess
        self.parent = parent
        self.children: Dict[Tuple[int, ...],
                            'MCTSNode'] = {}  # feedback -> node
        self.visits = 0
        self.value = 0.0
        self.untried_moves: List[str] = []

    def add_child(self, guess: str, feedback: Tuple[int, ...]) -> 'MCTSNode':
        """Add a child node with the given guess and feedback."""
        node = MCTSNode(guess=guess, parent=self)
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

    def __init__(self, dictionary_words: List[str], simulations: int = int(os.getenv('MCTS_SIMULATIONS', 10000))):
        """Initialize the solver.

        Args:
            dictionary_words: List of valid 5-letter words
            simulations: Number of MCTS simulations to run (default: 100000)
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

            # Selection
            while node.untried_moves == [] and node.children:
                node = self._select_ucb(node)

            # Expansion
            if node.untried_moves:
                guess = random.choice(node.untried_moves)
                node.untried_moves.remove(guess)

                # Simulate feedback
                target = random.choice(candidates)
                feedback = compute_feedback(guess, target)

                # Create new node
                node = node.add_child(guess, feedback)

            # Simulation
            result = self._simulate(node, candidates)

            # Backpropagation
            while node is not None:
                node.update(result)
                node = node.parent

        # Choose best move (most visited child)
        best_visits = -1
        best_guess = None

        for feedback, child in root.children.items():
            if child.visits > best_visits:
                best_visits = child.visits
                best_guess = child.guess

        return best_guess if best_guess else candidates[0]

    def _select_ucb(self, node: MCTSNode) -> MCTSNode:
        """Select a child node using UCB1."""
        best_score = float('-inf')
        best_child = None

        for child in node.children.values():
            score = child.get_ucb()
            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def _simulate(self, node: MCTSNode, candidates: List[str]) -> float:
        """Run a random simulation from the current node.

        Args:
            node: Current node in the search tree
            candidates: List of currently valid candidate words

        Returns:
            Score between 0 and 1 (1 is better)
        """
        if not candidates:
            return 0.0

        remaining = len(candidates)
        max_remaining = len(self.dictionary)

        # Score based on how much the candidate set was reduced
        # (normalized between 0 and 1, where 1 is better)
        return 1.0 - (remaining / max_remaining)

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

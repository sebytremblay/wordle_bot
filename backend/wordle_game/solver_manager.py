import config
from wordle_game.dictionary import load_dictionary
from typing import Dict, Any, List, Optional, Type, Tuple
from .solver import (
    BaseSolver,
    NaiveSolver,
    GreedySolver,
    MinimaxSolver,
    MCTSSolver
)
import math


class SolverManager:
    """Manages multiple solvers for a single game."""

    def __init__(self, dictionary_words: List[str]):
        """Initialize the solver manager.

        Args:
            dictionary_words: List of valid 5-letter words
        """
        self.dictionary = dictionary_words
        self._solvers: Dict[str, BaseSolver] = {}
        self._active_solver: Optional[BaseSolver] = None
        self.ordered_words = load_dictionary(config.ORDERED_WORDS_PATH) \
            if config.ORDERED_WORDS_PATH \
            else MinimaxSolver._estimate_feedback_spread(self.dictionary)

    def get_solver(self, solver_type: str, solver_params: Optional[Dict[str, Any]] = None) -> BaseSolver:
        """Get or create a solver of the specified type.

        Args:
            solver_type: Type of solver to get/create
            solver_params: Optional parameters for the solver:
                MCTS specific:
                    - simulations: Number of simulations
                    - exploration_constant: UCB1 exploration parameter
                    - reward_multiplier: Reward scaling factor
                Minimax specific:
                    - max_depth: Maximum search depth

        Returns:
            The requested solver instance
        """
        solver_type = solver_type.lower()
        solver_params = solver_params or {}

        # Create solver key that includes parameter hash for caching
        solver_key = solver_type
        if solver_params:
            param_hash = hash(frozenset(solver_params.items()))
            solver_key = f"{solver_type}_{param_hash}"

        # Create solver if it doesn't exist
        if solver_key not in self._solvers:
            solver_class = self._get_solver_class(solver_type)
            solver = self.create_solver(
                solver_class, self.dictionary, solver_params)
            self._solvers[solver_key] = solver

        return self._solvers[solver_key]

    def get_hint(self, candidates: List[str], previous_guesses: set[str], solver_type: Optional[str] = None, first_guess: bool = False, solver_params: Optional[Dict[str, Any]] = None) -> Tuple[str, str, int]:
        """Get a hint using the specified or active solver.

        Args:
            candidates: List of remaining candidate words
            previous_guesses: Set of previously guessed words
            solver_type: Optional solver type to use. If None, uses active solver.
            first_guess: Whether this is the first guess
            solver_params: Optional parameters for the solver

        Returns:
            Tuple containing:
                - The suggested word
                - The solver type used
                - Number of remaining candidates
        """
        # Use specified solver or current active solver
        if solver_type:
            solver = self.get_solver(solver_type, solver_params)
            self._active_solver = solver
        else:
            if not self._active_solver:
                self._active_solver = self.get_solver(config.DEFAULT_SOLVER)
            solver = self._active_solver

        # Get hint from solver
        hint = solver.starting_word() \
            if first_guess \
            else solver.select_guess(candidates)

        # Handle case where hint has already been guessed
        if hint in previous_guesses:
            # Try to find unguessed word from candidates
            for word in candidates:
                if word not in previous_guesses:
                    hint = word
                    break

            # If all candidates guessed, find any unguessed dictionary word
            if hint in previous_guesses:
                for word in self.dictionary:
                    if word not in previous_guesses:
                        hint = word
                        break

        return hint, solver.get_name(), len(candidates)

    @staticmethod
    def _get_solver_class(solver_type: str) -> Type[BaseSolver]:
        """Get the solver class based on type."""
        solvers = {
            NaiveSolver.get_name(): NaiveSolver,
            GreedySolver.get_name(): GreedySolver,
            MinimaxSolver.get_name(): MinimaxSolver,
            MCTSSolver.get_name(): MCTSSolver
        }

        solver_class = solvers.get(solver_type)
        if not solver_class:
            raise ValueError(f"Unknown solver type: {solver_type}")

        return solver_class

    def create_solver(self, solver_class: Type[BaseSolver], dictionary: List[str], solver_params: Optional[Dict[str, Any]] = None) -> BaseSolver:
        """Create a new solver instance with appropriate parameters.

        Args:
            solver_class: The solver class to instantiate
            dictionary: List of valid words
            solver_params: Optional parameters for the solver
        """
        if solver_class == MinimaxSolver:
            return solver_class(
                dictionary,
                self.ordered_words,
                max_depth=solver_params.get('max_depth', config.MINIMAX_DEPTH),
            )
        elif solver_class == MCTSSolver:
            return solver_class(
                dictionary,
                self.ordered_words,
                simulations=solver_params.get(
                    'simulations', config.MCTS_SIMULATIONS),
                exploration_constant=solver_params.get(
                    'exploration_constant', config.MCTS_EXPLORATION_CONSTANT),
                reward_multiplier=solver_params.get(
                    'reward_multiplier', config.MCTS_REWARD_MULTIPLIER)
            )
        else:
            return solver_class()

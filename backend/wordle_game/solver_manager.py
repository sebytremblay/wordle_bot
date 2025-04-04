import config
import inspect
from wordle_game.dictionary import load_dictionary
from typing import Dict, Any, List, Optional, Type, Tuple
from .solver import (
    BaseSolver,
    NaiveSolver,
    GreedySolver,
    MinimaxSolver,
    MCTSSolver
)


class SolverManager:
    """Manages multiple solvers for a single game."""

    def __init__(self, dictionary_words: List[str], is_wordle_list):
        """Initialize the solver manager.

        Args:
            dictionary_words: List of valid 5-letter words
        """
        self.dictionary = dictionary_words
        self.is_wordle_list = is_wordle_list
        self._solvers: Dict[str, BaseSolver] = {}
        self._active_solver: Optional[BaseSolver] = None

    def get_solver(self, solver_type: str) -> BaseSolver:
        """Get or create a solver of the specified type.

        Args:
            solver_type: Type of solver to get/create

        Returns:
            The requested solver instance
        """
        solver_type = solver_type.lower()

        # Create solver if it doesn't exist
        if solver_type not in self._solvers:
            solver_class = self._get_solver_class(solver_type)
            solver = SolverManager.create_solver(
                solver_class, self.dictionary, self.is_wordle_list)
            self._solvers[solver_type] = solver

        return self._solvers[solver_type]

    def get_hint(self, candidates: List[str], previous_guesses: set[str], solver_type: Optional[str] = None) -> Tuple[str, str, int]:
        """Get a hint using the specified or active solver.

        Args:
            candidates: List of remaining candidate words
            previous_guesses: Set of previously guessed words
            solver_type: Optional solver type to use. If None, uses active solver.

        Returns:
            Tuple containing:
                - The suggested word
                - The solver type used
                - Number of remaining candidates
        """
        # Use specified solver or current active solver
        if solver_type:
            solver = self.get_solver(solver_type)
            self._active_solver = solver
        else:
            if not self._active_solver:
                self._active_solver = self.get_solver(config.DEFAULT_SOLVER)
            solver = self._active_solver

        # Get hint from solver
        hint = solver.select_guess(candidates)

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

    @staticmethod
    def create_solver(solver_class: Type[BaseSolver], dictionary: List[str], is_wordle_list: bool = False) -> BaseSolver:
        """Create a new solver instance with appropriate parameters."""
        if solver_class == MinimaxSolver:
            if is_wordle_list:
                ordered_words = load_dictionary(config.ORDERED_WORDS_PATH)
            else:
                ordered_words = MinimaxSolver._estimate_feedback_spread(
                    dictionary)
            return solver_class(ordered_words)
        elif solver_class == MCTSSolver:
            return solver_class(dictionary, simulations=config.MCTS_SIMULATIONS)
        else:
            return solver_class()

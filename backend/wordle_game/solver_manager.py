import config
import inspect
from wordle_game.dictionary import load_dictionary
from typing import Dict, Any, List, Optional, Type
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
        self._active_solver: Optional[str] = None

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
            solver = SolverManager.create_solver(solver_class, self.dictionary, self.is_wordle_list)
            self._solvers[solver_type] = solver

        self._active_solver = solver_type
        return self._solvers[solver_type]

    def get_active_solver(self) -> Optional[BaseSolver]:
        """Get the currently active solver."""
        return self._solvers.get(self._active_solver) if self._active_solver else None

    @staticmethod
    def _get_solver_class(solver_type: str) -> Type[BaseSolver]:
        """Get the solver class based on type."""
        solvers = {
            NaiveSolver.solver_type(): NaiveSolver,
            GreedySolver.solver_type(): GreedySolver,
            MinimaxSolver.solver_type(): MinimaxSolver,
            MCTSSolver.solver_type(): MCTSSolver
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
                ordered_words = MinimaxSolver._estimate_feedback_spread(dictionary)
            return solver_class(ordered_words)
        elif solver_class == MCTSSolver:
            return solver_class(dictionary, simulations=config.MCTS_SIMULATIONS)
        else:
            return solver_class()

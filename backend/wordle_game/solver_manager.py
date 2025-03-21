from typing import Dict, Any, List, Tuple, Optional
from .solver import (
    BaseSolver,
    NaiveSolver,
    GreedySolver,
    MinimaxSolver,
    MCTSSolver
)


class SolverManager:
    """Manages multiple solvers for a single game."""

    def __init__(self, dictionary_words: List[str]):
        """Initialize the solver manager.

        Args:
            dictionary_words: List of valid 5-letter words
        """
        self.dictionary = dictionary_words
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
            solver = self._create_solver(solver_class)
            self._solvers[solver_type] = solver

        self._active_solver = solver_type
        return self._solvers[solver_type]

    def get_active_solver(self) -> Optional[BaseSolver]:
        """Get the currently active solver."""
        return self._solvers.get(self._active_solver) if self._active_solver else None

    def _get_solver_class(self, solver_type: str) -> Any:
        """Get the solver class based on type."""
        solvers = {
            "naive": NaiveSolver,
            "greedy": GreedySolver,
            "minimax": MinimaxSolver,
            "mcts": MCTSSolver
        }

        solver_class = solvers.get(solver_type)
        if not solver_class:
            raise ValueError(f"Unknown solver type: {solver_type}")

        return solver_class

    def _create_solver(self, solver_class: Any) -> BaseSolver:
        """Create a new solver instance with appropriate parameters."""
        if solver_class == MinimaxSolver:
            return solver_class(self.dictionary, max_depth=3)
        elif solver_class == MCTSSolver:
            return solver_class(self.dictionary, simulations=1000)
        else:
            return solver_class(self.dictionary)

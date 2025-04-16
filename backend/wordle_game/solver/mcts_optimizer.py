"""Hyperparameter optimization for the MCTS solver using Optuna."""

import random
import optuna
from typing import List, Dict, Any

from ..wordle_game import WordleGame
from ..solver_manager import SolverManager
from ..dictionary import load_dictionary
import config


class MCTSSolverOptimizer:
    def objective(self, trial: optuna.Trial, test_subset: List[str], solver_manager: SolverManager, dictionary: List[str]) -> float:
        """Objective function for Optuna optimization.

        Args:
            trial: Optuna trial object
            test_subset: List of possible target words
            solver_manager: SolverManager object
            dictionary: List of valid words
            n_test_games: Number of games to test per parameter set

        Returns:
            Average score (higher is better)
        """
        # Sample hyperparameters
        params = {
            'simulations': trial.suggest_int('simulations', 10, 250),
            'exploration_constant': trial.suggest_float('exploration_constant', 0.01, 10.0),
            'reward_multiplier': trial.suggest_float('reward_multiplier', 0.01, 100.0)
        }

        # Set guesses to high number to ensure all games are played to end
        max_guesses = 500

        # Test solver on each word
        total_guesses = 0
        for target_word in test_subset:
            game = WordleGame(dictionary, max_guesses, target_word)
            solver = solver_manager.get_solver(
                f'mcts_{config.MCTS_SIMULATIONS}', params)  # string key used only for identification, parameter loaded from params

            # Play game
            while not game.is_game_over():
                guess = solver.select_guess(game.candidate_words)
                game.submit_guess(guess)

            # Calculate score components
            total_guesses += game.guess_count

        # Score by average guesses
        avg_guesses = total_guesses / len(test_subset)
        trial.report(avg_guesses, step=0)
        if trial.should_prune():
            raise optuna.TrialPruned()

        return avg_guesses

    def optimize_mcts_parameters(self, n_trials: int = 50, n_test_games: int = 100) -> Dict[str, Any]:
        """Run hyperparameter optimization for MCTS solver.

        Args:
            n_trials: Number of optimization trials
            n_test_games: Number of games to test per parameter set

        Returns:
            Dictionary containing:
                - best_params: Best hyperparameters found
                - study: Optuna study object with optimization history
        """
        # Load dictionary and test words
        dictionary = load_dictionary(config.DICTIONARY_PATH)
        test_words = load_dictionary(config.WORDLE_ANS_PATH)

        # Create testing subset
        random.seed(config.RANDOM_SEED)
        test_subset = random.sample(test_words, n_test_games)

        # Create study object
        study = optuna.create_study(
            direction="minimize",
            sampler=optuna.samplers.TPESampler(seed=config.RANDOM_SEED),
            pruner=optuna.pruners.MedianPruner()
        )

        # Initialize solver manager
        solver_manager = SolverManager(dictionary)

        # Run optimization
        study.optimize(
            lambda trial: self.objective(
                trial, test_subset, solver_manager, dictionary),
            n_trials=n_trials,
            n_jobs=-1
        )

        return {
            "best_params": study.best_params,
            "study": study
        }


if __name__ == "__main__":
    optimizer = MCTSSolverOptimizer()
    print(optimizer.optimize_mcts_parameters())

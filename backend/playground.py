"""A playground file for testing and experimenting with the code.

This file provides examples of how to use different Wordle solvers and run games locally.
It includes examples for all available solver types and demonstrates their usage.
"""
import random
from wordle_game.solver.base_solver import BaseSolver
import config

from typing import List
import time
from cache_service.hint_cache import HintCache
from wordle_game.wordle_game import WordleGame
from wordle_game.dictionary import load_dictionary
from wordle_game.solver import (
    NaiveSolver,
    GreedySolver,
    MinimaxSolver,
    MCTSSolver
)
from wordle_game.solver_manager import SolverManager


def run_single_game(solver: BaseSolver, dictionary: List[str], target_word: str) -> tuple[bool, int]:
    """Run a single Wordle game with the given solver and target word.

    Args:
        solver: A Wordle solver instance
        target_word: The target word to guess

    Returns:
        tuple[bool, int]: (whether game was won, number of guesses used)
    """
    game = WordleGame(dictionary.copy(), target_word=target_word)

    # Define hint computation function
    def compute_hint():
        hint, _, _ = game.get_hint(solver.solver_type())
        return hint

    while not game.is_game_over():
        # Get a hint from cache if exists, compute otherwise
        guess, _ = HintCache.get_or_compute_hint(
            game_state=game.get_game_state(),
            solver_type=solver.solver_type(),
            compute_fn=compute_hint
        )

        # Submit guess to game
        game.submit_guess(guess)

    return game.game_won, game.guess_count


def demo_solver(solver_class: BaseSolver, dictionary: List[str], test_words: List[str]):
    """Demonstrate a solver's performance on some test words.

    Args:
        solver_class: The solver class to test
        dictionary: List of valid words
        test_words: List of target words to test
    """
    solver = SolverManager.create_solver(solver_class, dictionary)
    print(f"Solver Class Name: {solver.solver_type()}")

    print(f"\nTesting {solver.solver_type()} solver:")
    print("-" * 40)

    total_guesses = 0
    wins = 0
    start_time = time.time()

    for word in test_words:
        won, guesses = run_single_game(solver, dictionary, word)
        wins += int(won)
        total_guesses += guesses
        print(
            f"Target: {word:6} | {'Won' if won else 'Lost'} in {guesses} guesses")

    end_time = time.time()
    avg_guesses = total_guesses / len(test_words)
    win_rate = (wins / len(test_words)) * 100

    print(f"\nResults:")
    print(f"Win rate: {win_rate:.1f}%")
    print(f"Average guesses: {avg_guesses:.2f}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")


def main(num_test_words: int = 5):
    """Main function to demonstrate different solvers."""
    dictionary = load_dictionary(config.DICTIONARY_PATH)

    # For quick testing, we'll use a random sample
    test_words = random.sample(dictionary, num_test_words)

    # Test each solver type
    solvers = [
        NaiveSolver,
        GreedySolver,
        MinimaxSolver,
        MCTSSolver
    ]

    for solver_class in solvers:
        demo_solver(solver_class, dictionary, test_words)


if __name__ == "__main__":
    main(5)

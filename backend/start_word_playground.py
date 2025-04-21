"""
A playground file for testing and experimenting with the code.

Tests different starting words against a list of words using selected solvers.
Tracks if word was solved within 6 attempts, but continues until solved.
Includes caching for GreedySolver to improve speed.
"""

import time
import sys
from collections import defaultdict
import statistics
from typing import Type, List

from wordle_game.solver.base_solver import BaseSolver
import config
from web_interface.app_session import AppSession
from wordle_game.dictionary import load_dictionary
from wordle_game.solver import (
    NaiveSolver,
    GreedySolver,
    MinimaxSolver,
    MCTSSolver
)
from wordle_game.solver_manager import SolverManager

MAX_GUESSES = 15

PARTITIONS_CACHE = {}
INFO_GAIN_CACHE = {}

# Define solver parameters
SOLVER_PARAMS = {
    NaiveSolver: None,
    GreedySolver: None,
    MinimaxSolver: {'max_depth': config.MINIMAX_DEPTH},
    MCTSSolver: {
        'simulations': config.MCTS_SIMULATIONS,
        'exploration_constant': config.MCTS_EXPLORATION_CONSTANT,
        'reward_multiplier': config.MCTS_REWARD_MULTIPLIER
    }
}


def add_caching_to_greedy():
    """Add caching to GreedySolver methods."""
    GreedySolver._original_partitions = GreedySolver._compute_partitions
    GreedySolver._original_info_gain = GreedySolver._compute_expected_info_gain

    def cached_partitions(self, guess, candidates):
        key = (guess, frozenset(candidates))
        if key not in PARTITIONS_CACHE:
            PARTITIONS_CACHE[key] = self._original_partitions(guess, candidates)
        return PARTITIONS_CACHE[key]

    def cached_info_gain(self, guess, candidates):
        key = (guess, frozenset(candidates))
        if key not in INFO_GAIN_CACHE:
            INFO_GAIN_CACHE[key] = self._original_info_gain(guess, candidates)
        return INFO_GAIN_CACHE[key]

    GreedySolver._compute_partitions = cached_partitions
    GreedySolver._compute_expected_info_gain = cached_info_gain


def remove_caching_from_greedy():
    """Remove caching from GreedySolver methods."""
    if hasattr(GreedySolver, '_original_partitions'):
        GreedySolver._compute_partitions = GreedySolver._original_partitions
        GreedySolver._compute_expected_info_gain = GreedySolver._original_info_gain


def run_game_with_fixed_start(solver: BaseSolver, dictionary: List[str], target_word: str, first_guess: str):
    """Run a Wordle game starting with a fixed first guess."""
    session = AppSession(
        dictionary_words=dictionary.copy(),
        target_word=target_word,
        max_guesses=MAX_GUESSES,
    )

    found_word = False
    total_guesses = 0
    guess_list = []

    # Submit first guess
    session.submit_guess(first_guess)
    guess_list.append(first_guess)
    total_guesses += 1

    if first_guess == target_word:
        return True, total_guesses, guess_list

    def compute_hint():
        hint, _, _ = session.get_hint(solver.get_name())
        return hint

    while not found_word:
        if total_guesses >= session.game_state.max_guesses:
            return False, total_guesses, guess_list

        guess = compute_hint()
        guess_list.append(guess)
        session.submit_guess(guess)
        total_guesses += 1

        if guess == target_word:
            found_word = True

    win_within_6 = total_guesses <= 6
    return win_within_6, total_guesses, guess_list


def test_starting_word(solver_manager: SolverManager, solver_class: Type[BaseSolver], start_word: str, dictionary: List[str], test_words: List[str]):
    """Test a starting word with a given solver over multiple target words."""
    if solver_class == GreedySolver:
        add_caching_to_greedy()

    try:
        solver = solver_manager.create_solver(solver_class, dictionary, SOLVER_PARAMS)
        solver_name = solver.get_name()
        print(f"Testing '{start_word}' with {solver_name}...")

        total_guesses = 0
        wins_within_6 = 0
        guess_counts = []
        guess_distribution = defaultdict(int)
        long_guess_cases = {}

        start_time = time.time()

        for i, word in enumerate(test_words):
            progress = i / len(test_words) * 100
            sys.stdout.write(f"\r{progress:.1f}% complete...")
            sys.stdout.flush()

            try:
                win_within_6, guesses, guess_list = run_game_with_fixed_start(
                    solver, dictionary, word, start_word
                )
                wins_within_6 += int(win_within_6)
                total_guesses += guesses
                guess_counts.append(guesses)
                guess_distribution[guesses] += 1
                if guesses > 10:
                    long_guess_cases[word] = guess_list
            except Exception as e:
                print(f"\nError on word '{word}': {str(e)}")
                continue

        end_time = time.time()

        win_rate = (wins_within_6 / len(test_words)) * 100
        avg_guesses = total_guesses / len(guess_counts) if guess_counts else 0
        median_guesses = statistics.median(guess_counts) if guess_counts else 0
        time_taken = end_time - start_time

        print("\n\nResults:")
        print(f"Starting Word: {start_word}")
        print(f"Win rate (≤6): {win_rate:.1f}%")
        print(f"Average guesses: {avg_guesses:.2f}")
        print(f"Median guesses: {median_guesses}")
        print(f"Time taken: {time_taken:.2f}s")

        print("Guess Distribution:")
        for num_guesses in sorted(guess_distribution):
            count = guess_distribution[num_guesses]
            print(f"{num_guesses}: {count}")

        return {
            "start_word": start_word,
            "solver": solver_name,
            "win_rate": win_rate,
            "avg_guesses": avg_guesses,
            "median_guesses": median_guesses,
            "time_taken": time_taken
        }

    finally:
        if solver_class == GreedySolver:
            remove_caching_from_greedy()


def main():
    dictionary = load_dictionary(config.DICTIONARY_PATH)
    test_words = load_dictionary(config.WORDLE_ANS_PATH)
    test_words = ["lathe"]

    print("Enter comma-separated starting words (e.g. 'slate,crane,adieu'):")
    input_words = input("Starting words: ").strip().lower()
    starting_words = [word.strip() for word in input_words.split(",")]

    print("\nWhich solver to use?")
    print("1. GreedySolver")
    print("2. MinimaxSolver")
    print("3. MCTSSolver")
    print("4. NaiveSolver")
    print("5. All Solvers")
    choice = input("Enter choice (1-5): ")

    solver_map = {
        "1": GreedySolver,
        "2": MinimaxSolver,
        "3": MCTSSolver,
        "4": NaiveSolver,
        "5": [NaiveSolver, GreedySolver, MinimaxSolver, MCTSSolver]
    }

    solvers = solver_map.get(choice, GreedySolver)

    solver_manager = SolverManager(dictionary)
    results = []

    for solver_class in solvers:
        for start_word in starting_words:
            result = test_starting_word(
                solver_manager, solver_class, start_word, dictionary, test_words
            )
            results.append(result)

    if len(results) > 1:
        print("\n" + "=" * 60)
        print("STARTING WORD COMPARISON")
        print("=" * 60)
        print(
            f"{'Word':<10} {'Solver':<12} {'Win Rate (≤6)':<15} {'Avg Guesses':<15} {'Median':<10} {'Time (s)':<10}")
        for r in results:
            print(f"{r['start_word']:<10} {r['solver']:<12} {r['win_rate']:.1f}%{' ':9} {r['avg_guesses']:.2f}{' ':10} {r['median_guesses']:<10} {r['time_taken']:.2f}")


if __name__ == "__main__":
    main()
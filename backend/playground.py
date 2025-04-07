"""A playground file for testing and experimenting with the code.

Tests solvers against a list of words with no guess limit.
Tracks if word was solved within 6 attempts, but continues until solved.
Includes caching for GreedySolver to improve speed.
"""
import random
import time
import sys
from collections import defaultdict
import statistics
from typing import Type, List

from wordle_game.solver.base_solver import BaseSolver
import config
from cache_service.hint_cache import HintCache
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

# cache for greedy
PARTITIONS_CACHE = {}
INFO_GAIN_CACHE = {}


def add_caching_to_greedy():
    """Add caching to GreedySolver methods."""
    # save original methods
    GreedySolver._original_partitions = GreedySolver._compute_partitions
    GreedySolver._original_info_gain = GreedySolver._compute_expected_info_gain

    # create cached version of partitions method
    def cached_partitions(self, guess, candidates):
        key = (guess, frozenset(candidates))
        if key not in PARTITIONS_CACHE:
            PARTITIONS_CACHE[key] = self._original_partitions(
                guess, candidates)
        return PARTITIONS_CACHE[key]

    # create cached version of info gain method
    def cached_info_gain(self, guess, candidates):
        key = (guess, frozenset(candidates))
        if key not in INFO_GAIN_CACHE:
            INFO_GAIN_CACHE[key] = self._original_info_gain(guess, candidates)
        return INFO_GAIN_CACHE[key]

    # replace methods with cached versions
    GreedySolver._compute_partitions = cached_partitions
    GreedySolver._compute_expected_info_gain = cached_info_gain


def remove_caching_from_greedy():
    """Remove caching from GreedySolver methods."""
    if hasattr(GreedySolver, '_original_partitions'):
        GreedySolver._compute_partitions = GreedySolver._original_partitions
        GreedySolver._compute_expected_info_gain = GreedySolver._original_info_gain


def run_game_no_limit(solver: BaseSolver, dictionary: List[str], target_word: str):
    """Run a Wordle game with no guess limit.

    Args:
        solver: The solver instance
        dictionary: The dictionary of valid words
        target_word: The target word to guess

    Returns:
        tuple: (win_within_6, total_guesses)
    """
    session = AppSession(
        dictionary_words=dictionary.copy(),
        target_word=target_word,
        max_guesses=MAX_GUESSES,
    )

    def compute_hint():
        hint, _, _ = session.get_hint(solver.get_name())
        return hint

    found_word = False
    total_guesses = 0
    guess_list = []

    while not found_word:
        try:
            # Try to use cache
            guess, _ = HintCache.get_or_compute_hint(
                game_state=session.get_game_state(),
                solver_type=solver.get_name(),
                compute_fn=compute_hint
            )
        except Exception as e:
            # If cache fails, compute directly
            guess = compute_hint()

        guess_list.append(guess)

        # Submit guess
        if total_guesses >= session.game_state.max_guesses:
            return False, total_guesses, guess_list

        session.submit_guess(guess)
        total_guesses += 1

        # Check if word found
        if guess == target_word:
            found_word = True

    # Word guessed within 6 attempts is considered a win
    win_within_6 = (total_guesses <= 6)

    return win_within_6, total_guesses, guess_list


def test_solver(solver_manager: SolverManager, solver_class: Type[BaseSolver], dictionary: List[str], test_words: List[str], print_hard_words: bool = True):
    """Test a solver on multiple words and report results."""
    # Add caching for GreedySolver
    if solver_class == GreedySolver:
        add_caching_to_greedy()

    try:
        solver = solver_manager.create_solver(
            solver_class, dictionary)
        solver_name = solver.get_name()

        print(f"Testing {solver_name} solver...")

        total_guesses = 0
        wins_within_6 = 0
        guess_counts = []
        guess_distribution = defaultdict(int)
        long_guess_cases = {}

        start_time = time.time()

        # Test each word
        for i, word in enumerate(test_words):
            # Show progress
            progress = i / len(test_words) * 100
            sys.stdout.write(f"\r{progress:.1f}% complete...")
            sys.stdout.flush()

            try:
                win_within_6, guesses, guess_list = run_game_no_limit(
                    solver, dictionary, word)
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

        print("\nResults:")
        print(f"Win rate (6 guesses or less): {win_rate:.1f}%")
        print(f"Average guesses needed: {avg_guesses:.2f}")
        print(f"Median guesses needed: {median_guesses}")
        print(f"Time taken: {time_taken:.2f} seconds")

        print("\nGuess Distribution:")
        for guesses, count in sorted(guess_distribution.items()):
            percentage = (count / len(guess_counts)) * 100
            if guesses >= MAX_GUESSES:
                print(f">={guesses}: {count} ({percentage:.1f}%)")
            else:
                print(f"{guesses}: {count} ({percentage:.1f}%)")

        if print_hard_words and long_guess_cases:
            print("\nWords that took more than 10 guesses:")
            for word, guesses in long_guess_cases.items():
                print(f"{word}: {guesses}")

        return {
            "solver": solver_name,
            "win_rate": win_rate,
            "avg_guesses": avg_guesses,
            "median_guesses": median_guesses,
            "time_taken": time_taken
        }

    finally:
        # Remove caching for GreedySolver
        if solver_class == GreedySolver:
            remove_caching_from_greedy()


def main():
    """Main function to test and compare solvers."""
    dictionary = load_dictionary(config.DICTIONARY_PATH)

    print("How many words to test?")
    print("1. Small sample (5 words)")
    print("2. Medium sample (25 words)")
    print("3. Large sample (100 words)")
    print("4. All words in valid wordle list")
    print("5. All wordle answers (before NYT bought Wordle)")
    choice = input("Enter choice (1-5): ")
    print()

    sample_size_map = {"1": 5, "2": 25, "3": 100, "4": 0, "5": -1}
    size = sample_size_map.get(choice, 0)
    if size > 0:
        test_words = random.sample(dictionary, size)
    elif size == 0:
        test_words = dictionary
    else:
        test_words = load_dictionary(config.WORDLE_ANS_PATH)

    print(f"Testing with {len(test_words)} words")

    print("\nWhich solvers to test?")
    print("1. All solvers")
    print("2. Only GreedySolver")
    print("3. Only MinimaxSolver")
    print("4. Only MCTSSolver")
    print("5. Only NaiveSolver")
    choice = input("Enter choice (1-5): ")

    solver_map = {
        "1": [NaiveSolver, GreedySolver, MinimaxSolver, MCTSSolver],
        "2": [GreedySolver],
        "3": [MinimaxSolver],
        "4": [MCTSSolver],
        "5": [NaiveSolver]
    }

    solvers = solver_map.get(choice, solver_map["1"])
    solver_manager = SolverManager(dictionary)
    results = []
    for solver_class in solvers:
        result = test_solver(solver_manager, solver_class,
                             dictionary, test_words)
        results.append(result)

    if len(results) > 1:
        print("\n" + "="*60)
        print("SOLVER COMPARISON")
        print("="*60)

        sorted_results = sorted(
            results, key=lambda x: (-x["win_rate"], x["avg_guesses"]))

        print(
            f"{'Solver':<10} {'Win Rate (≤6)':<15} {'Avg Guesses':<15} {'Median':<10} {'Time (s)':<10}")
        for r in sorted_results:
            print(f"{r['solver']:<10} {r['win_rate']:.1f}%{' ':9} {r['avg_guesses']:.2f}{' ':10} {r['median_guesses']:<10} {r['time_taken']:.2f}")


if __name__ == "__main__":
    main()

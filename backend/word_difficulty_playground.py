import sys
from typing import List

from wordle_game.solver.base_solver import BaseSolver
import config
from web_interface.app_session import AppSession
from wordle_game.dictionary import load_dictionary
from wordle_game.solver import *
from wordle_game.solver_manager import SolverManager

MAX_GUESSES = 15
PARTITIONS_CACHE = {}
INFO_GAIN_CACHE = {}


def add_caching_to_greedy():
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
    if hasattr(GreedySolver, '_original_partitions'):
        GreedySolver._compute_partitions = GreedySolver._original_partitions
        GreedySolver._compute_expected_info_gain = GreedySolver._original_info_gain


def run_game_with_fixed_start(solver: BaseSolver, dictionary: List[str], target_word: str, first_guess: str):
    session = AppSession(
        dictionary_words=dictionary.copy(),
        target_word=target_word,
        max_guesses=MAX_GUESSES,
    )

    guess_list = [first_guess]
    session.submit_guess(first_guess)
    if first_guess == target_word:
        return 1, guess_list

    def compute_hint():
        hint, _, _ = session.get_hint(solver.get_name())
        return hint

    while len(guess_list) < MAX_GUESSES:
        guess = compute_hint()
        guess_list.append(guess)
        session.submit_guess(guess)
        if guess == target_word:
            break

    return len(guess_list), guess_list


def main():
    dictionary = load_dictionary(config.DICTIONARY_PATH)
    test_words = load_dictionary(config.WORDLE_ANS_PATH)
    start_word = "slate"

    # add_caching_to_greedy()
    solver_manager = SolverManager(dictionary)
    # solver = solver_manager.create_solver(NaiveSolver, dictionary, {})
    # solver = solver_manager.create_solver(MinimaxSolver, dictionary, {})
    solver = solver_manager.create_solver(MCTSSolver, dictionary, {})
    print(f"Classifying with {solver.get_name()}")

    easy_words = []
    hard_words = []

    for i, word in enumerate(test_words):
        progress = i / len(test_words) * 100
        sys.stdout.write(f"\r{progress:.1f}% complete...")
        sys.stdout.flush()

        try:
            num_guesses, guess_list = run_game_with_fixed_start(solver, dictionary, word, start_word)
            entry = (word, num_guesses, guess_list)
            if num_guesses <= 3:
                easy_words.append(entry)
            elif num_guesses >= 8:
                hard_words.append(entry)
        except Exception as e:
            print(f"\nError on word '{word}': {str(e)}")

    print("\n\nEASY WORDS (≤3 guesses):")
    for word, guesses, guess_list in easy_words:
        print(f"{word}: {guesses} guesses -> {guess_list}")

    print("\nHARD WORDS (8+ guesses):")
    for word, guesses, guess_list in hard_words:
        print(f"{word}: {guesses} guesses -> {guess_list}")

    # remove_caching_from_greedy()


if __name__ == "__main__":
    main()
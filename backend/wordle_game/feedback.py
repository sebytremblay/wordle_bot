from functools import lru_cache
from typing import List, Tuple
from collections import Counter
import config


@lru_cache(maxsize=None)
def compute_feedback(guess: str, target: str) -> Tuple[int, ...]:
    """Compute Wordle feedback for a guess against a target word.

    Args:
        guess: The guessed word
        target: The target word

    Returns:
        Tuple of integers where:
            2 = correct letter in correct position (green)
            1 = correct letter in wrong position (yellow)
            0 = letter not in word (gray)
    """
    guess = guess.lower()
    target = target.lower()
    feedback = [0] * config.WORD_LENGTH

    # First pass: Mark correct positions (green)
    target_chars = list(target)
    for i in range(config.WORD_LENGTH):
        if guess[i] == target_chars[i]:
            feedback[i] = 2
            target_chars[i] = None  # Mark as used

    # Second pass: Mark correct letters in wrong positions (yellow)
    remaining_chars = Counter(
        char for char in target_chars if char is not None)
    for i in range(config.WORD_LENGTH):
        if feedback[i] == 0 and guess[i] in remaining_chars and remaining_chars[guess[i]] > 0:
            feedback[i] = 1
            remaining_chars[guess[i]] -= 1

    return tuple(feedback)


@lru_cache(maxsize=None)
def filter_candidates(candidates: Tuple[str, ...], guess: str, feedback: Tuple[int, ...]) -> Tuple[str, ...]:
    """Filter the candidate words based on the feedback from a guess.

    Args:
        candidates: List of possible target words
        guess: The word that was guessed
        feedback: Tuple of feedback values (2: green, 1: yellow, 0: gray)

    Returns:
        Filtered list of candidates that match the feedback pattern
    """
    filtered = []
    guess = guess.lower()
    gray_letters = {guess[i] for i, code in enumerate(feedback) if code == 0}

    # remove letters that appear elsewhere as yellow or green
    for i, code in enumerate(feedback):
        # if letter is green/yellow somewhere else
        if code > 0 and guess[i] in gray_letters:
            gray_letters.remove(guess[i])  # it's not really "gray"

    # filter words that contain any gray letters first
    filtered_candidates = [word for word in candidates if word != guess and not any(
        letter in gray_letters for letter in word)]

    # now apply feedback checking
    filtered = [word for word in filtered_candidates if matches_feedback(
        word, guess, feedback)]

    return tuple(filtered)


@lru_cache(maxsize=None)
def matches_feedback(word: str, guess: str, feedback: Tuple[int, ...]) -> bool:
    """Check if a word matches the feedback pattern from a guess.

    Args:
        word: Word to check
        guess: The guessed word
        feedback: Tuple of feedback values

    Returns:
        True if the word matches the feedback pattern
    """
    # Quick check: Correct positions (green) must match
    for i, (letter, code) in enumerate(zip(guess, feedback)):
        if code == 2 and word[i] != letter:
            return False

    # Count remaining letters for yellow checks
    word_chars = Counter(word)
    guess_chars = Counter()

    # Remove green matches from counts
    for i, (letter, code) in enumerate(zip(guess, feedback)):
        if code == 2:
            word_chars[letter] -= 1
            if word_chars[letter] == 0:
                del word_chars[letter]

    # Check yellow positions and build guess character counts
    for i, (letter, code) in enumerate(zip(guess, feedback)):
        if code == 1:
            guess_chars[letter] += 1
            # Letter must exist in remaining word characters
            if letter not in word_chars or word_chars[letter] < guess_chars[letter]:
                return False
        elif code == 0:
            # If the letter was marked as gray, it shouldn't appear in remaining positions
            # unless it appears elsewhere as yellow or green
            if letter in word_chars and word_chars[letter] > guess_chars[letter]:
                return False

    return True

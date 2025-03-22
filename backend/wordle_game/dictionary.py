from typing import List, Set
import os
import json


def load_dictionary(file_path: str) -> List[str]:
    """Load the dictionary of valid words from a file.

    Args:
        file_path: Path to the dictionary file (txt or json)

    Returns:
        List of valid 5-letter words
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dictionary file not found: {file_path}")

    words = []

    # Assume text file with one word per line
    with open(file_path, 'r') as f:
        words = [line.strip().lower() for line in f if line.strip()]

    # Validate and filter words
    valid_words = [word for word in words if is_valid_word(word)]

    if not valid_words:
        raise ValueError("No valid 5-letter words found in dictionary")

    return valid_words


def is_valid_word(word: str) -> bool:
    """Check if a word is valid for Wordle (5 letters, alphabetic).

    Args:
        word: Word to validate

    Returns:
        True if the word is valid
    """
    return (len(word) == 5 and
            word.isalpha() and
            word.isascii() and
            word.islower())

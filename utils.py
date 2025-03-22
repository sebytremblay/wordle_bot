import itertools
from abc import ABC, abstractmethod

class WordleBot(ABC):
    @abstractmethod
    def guess(self, feedback=None, last_guess=None, remaining_words=None, hardmode=True):
        pass  # each algorithm will implement this method

def generate_feedback(target_word, guessed_word):
    feedback = [2] * 5  # start with all grey
    target_char_count = {}
    for i in range(5):  # "green" matches
        if guessed_word[i] == target_word[i]:
            feedback[i] = 0
        else:
            target_char_count[target_word[i]] = target_char_count.get(target_word[i], 0) + 1
    for i in range(5):  # "yellow" matches
        if feedback[i] != 0:  # skip greens
            if guessed_word[i] in target_char_count and target_char_count[guessed_word[i]] > 0:
                feedback[i] = 1
                target_char_count[guessed_word[i]] -= 1
    return feedback

def filter_words(guess: str, feedback: list[int], remaining_words: list[str], eliminated_letters: set) -> list[str]:
    filtered_words = []
    for word in remaining_words:
        simulated_feedback = generate_feedback(word, guess)
        if simulated_feedback == feedback and not any(letter in eliminated_letters for letter in word):
            filtered_words.append(word)
    return filtered_words
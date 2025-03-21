from abc import ABC, abstractmethod
import random


class WordleBot(ABC):
    @abstractmethod
    def guess(self, feedback=None):
        pass # each algorithm will implement this method


class BaselineWordleBot(WordleBot):
      """
    A baseline Wordle bot that uses a naive, greedy approach
    It selects a random word from the remaining valid word list after filtering based on feedback.
    """
    def __init__(self, word_list):
          """
        Initializes the bot with the full list of possible words.
        
        :param word_list: List of valid words to choose from.
        """
        self.remaining_words = word_list.copy()
         # to keep track of eliminated letters
        self.eliminated_letters = set()
    
    def guess(self, feedback=None, previous_guess=None):
        """
        Makes a guess based on the remaining possible words.
        If feedback is provided, it filters the word list before making the next guess.
        
        :param feedback: List of integers (0=Green, 1=Yellow, 2=Grey) representing feedback.
        :param previous_guess: The last guessed word.
        :return: A randomly chosen word from the filtered word list.
        """
        if feedback and previous_guess:
            # Filter words based on feedback from the previous guess
            self.remaining_words = filter_words(previous_guess, feedback, self.remaining_words, self.eliminated_letters)
        
        if not self.remaining_words:
            raise ValueError("No words remaining after filtering! Check the logic")
        
        # Randomly select a word from the remaining possibilities
        return random.choice(self.remaining_words)


def generate_feedback(target_word, guessed_word):
    ## 0: Green
    ## 1: Yellow
    ## 2: Grey
    feedback = [2] * 5 # start with all grey
    target_char_count = {}
    for i in range(5): # "green" matches
        if guessed_word[i] == target_word[i]:
            feedback[i] = 0 
        else:
            target_char_count[target_word[i]] = target_char_count.get(target_word[i], 0) + 1
    for i in range(5): # "yellow" matches
        if feedback[i] != 0: # skip greens
            # dupe handling
            if guessed_word[i] in target_char_count and target_char_count[guessed_word[i]] > 0:
                feedback[i] = 1
                target_char_count[guessed_word[i]] -= 1 
    return feedback

def filter_words(guess: str, feedback: list[int], remaining_words: list[str], eliminated_letters: set) -> list[str]:
    # Ensure guessed word is removed from remaining words
    if feedback == 5*[0]:
        remaining_words = [guess]
    # else:
    #     remaining_words = [word for word in remaining_words if word != guess]

    # Filter out words that:
    # 1. Don't match the feedback.
    # 2. Contain any eliminated letters.
    filtered_words = []
    for word in remaining_words:
        simulated_feedback = generate_feedback(word, guess)
        # print(word, ":", simulated_feedback, "==", feedback)
        if simulated_feedback == feedback and not any(letter in eliminated_letters for letter in word):
            filtered_words.append(word)
    return filtered_words
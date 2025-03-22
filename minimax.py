from utils import *
import itertools

class MinimaxWordleBot(WordleBot):
    def __init__(self):
        self.attempts = 0
        self.eliminated_letters = set()
        self.word_list = load_words_from_file('ordered_words.txt')

    def guess(self, feedback, last_guess, remaining_words, hardmode=True):
        self.attempts += 1
        if last_guess is None:
            # arose = best word for information gain: entropy & diversity
            return "arose", self.attempts
        if feedback and last_guess:
            remaining_words = filter_words(last_guess, feedback, remaining_words, self.eliminated_letters)
        
        guessed_word = None
        if not hardmode:
            guess_easy, easy_word = should_make_easy_guess(remaining_words, self.eliminated_letters, self.word_list)
            if guess_easy:
                guessed_word = easy_word
        if not guessed_word:
            guessed_word, _, _ = minimax(remaining_words)

        return guessed_word, self.attempts
    
def should_make_easy_guess(remaining_words, eliminated_letters, word_list):
    # filter out words that contain eliminated letters from word_list
    filtered_word_list = [word for word in word_list if not any(letter in eliminated_letters for letter in word)]
    best_score = float('inf')  # Initialize with the worst possible score
    best_guess = None  # Initialize the best guess
    for guess_word in filtered_word_list:
        groupings = {} # groupings based on feedback for each remaining word
        for word in remaining_words:
            feedback = tuple(generate_feedback(guess_word, word))
            if feedback not in groupings:
                groupings[feedback] = []
            groupings[feedback].append(word)
        # worst-case scenario (largest group size for any feedback) for this guess
        worst_case = max(len(group) for group in groupings.values())
        # minimax: choose the guess that minimizes the worst-case scenario
        if worst_case < best_score:
            best_score = worst_case
            best_guess = guess_word
    return best_score < len(remaining_words), best_guess

def minimax(remaining_words, prune=True, alpha=float('-inf'), beta=float('inf')):
    if not remaining_words:
        raise ValueError("Remaining words list is empty.")
    ## select the guess that minimizes the maximum number of remaining words in the worst-case scenario.
    best_score = float('inf') # min score better -> fewer words remaining
    best_guess = remaining_words[0]
    best_outcomes = None

    for guess in remaining_words:
        outcomes = get_outcomes(guess, remaining_words)
        worst_case = max(len(words) for words in outcomes.values())
        # worst case -> largest group of remaining words for a feedback combinatio
        if worst_case < best_score:
            best_score = worst_case
            best_guess = guess
            best_outcomes = outcomes
            if prune: alpha = max(alpha, best_score)

        if prune and beta <= alpha:
            break  # prune

    return best_guess, best_score, best_outcomes

def get_outcomes(guess: str, remaining_words: list[str]) -> dict[tuple[str], list[str]]:
    outcomes = {}
    # all feedback combinations (permutations with repetition for 5-letter words)
    for combination in itertools.product([0, 1, 2], repeat=5):
        outcomes[combination] = []

    # store feedback for each word in remaining_words with the corresponding outcome combination
    for word in remaining_words:
        feedback = tuple(generate_feedback(word, guess))
        outcomes[feedback].append(word)

    return outcomes

def load_words_from_file(file_path):
    with open(file_path, 'r') as file:
        words = [line.strip() for line in file if line.strip() and not line.startswith('#')]
    return words

def letter_set_similarity(word, other_words):
    ## estimates feedback spread by counting overlaps with other words
    word_set = set(word)
    score = sum(len(word_set & set(other)) for other in other_words)
    return score / len(other_words)

def estimate_feedback_spread(words):
    ## ranks words with heuristic to maximize pruning
    estimated_scores = {word: letter_set_similarity(word, words) for word in words}
    return sorted(words, key=lambda w: (-estimated_scores[w], -len(set(w))))

def guess_word(target, bot, hardmode=True, verbose=False):
    remaining_words = bot.word_list
    guess, feedback = None, None
    while guess != target:
        guess, attempt = bot.guess(feedback, guess, remaining_words, hardmode)
        if verbose: print(f"Bot guessed: {guess}, Attempts: {attempt}")
        feedback = generate_feedback(target, guess)
        if verbose: print(f"Feedback for guess '{guess}': {feedback}")
        # update eliminated letters based on feedback
        for i in range(len(feedback)):
            if feedback[i] == 2 and guess[i] not in bot.eliminated_letters:
                if guess[i+1:].count(guess) > 1:
                    if verbose: print(bot.eliminated_letters)
                    print(guess[i+1:])
                    bot.eliminated_letters.add(guess[i])
        # filter remaining words based on new feedback
        remaining_words = filter_words(guess, feedback, remaining_words, bot.eliminated_letters)
        if verbose: print(f"Remaining words after filtering: {remaining_words}")
    if verbose: print("Bot guessed the correct word (", target,") in", attempt, "guesses!")
    return attempt
    
## Below code was used to create 'ordered_words.txt'
# def save_words_to_file(words, file_path):
#     with open(file_path, 'w') as file:
#         for word in words:
#             file.write(word + '\n')
# word_list = load_words_from_file('words.txt')
# ordered_words = estimate_feedback_spread(word_list)
# save_words_to_file(ordered_words, 'ordered_words.txt')

bot = MinimaxWordleBot()
guess_word("words", bot, True, True)
from utils import WordleBot, generate_feedback, filter_words
import itertools

class MinimaxWordleBot(WordleBot):
    def __init__(self):
        self.attempts = 0
        self.eliminated_letters = set()

    def guess(self, feedback, last_guess, remaining_words):
        self.attempts += 1
        if last_guess is None:
            # arose = best word for information gain: entropy & diversity
            return "arose", self.attempts
        if feedback and last_guess:
            remaining_words = filter_words(last_guess, feedback, remaining_words, self.eliminated_letters)
        guessed_word, _, _ = minimax_alpha_beta(remaining_words)
        return guessed_word, self.attempts

def minimax_alpha_beta(remaining_words, alpha=float('-inf'), beta=float('inf')):
    best_score = float('inf')
    best_guess = remaining_words
    best_outcomes = None

    for guess in remaining_words:
        outcomes = get_outcomes(guess, remaining_words)
        worst_case = max(len(words) for words in outcomes.values())

        if worst_case < best_score:
            best_score = worst_case
            best_guess = guess
            best_outcomes = outcomes
            alpha = max(alpha, best_score)

        if beta <= alpha:
            break  # prune

    return best_guess, best_score, best_outcomes

def minimax(candidate_words: list[str], remaining_words: list[str]):
    ## select the guess that minimizes the maximum number of remaining words in the worst-case scenario.
    best_score = float('inf')  # min score better -> fewer words remaining
    best_guess, best_outcomes = None, None
    outcomes = {}
    
    for guess in candidate_words:
        outcomes = get_outcomes(guess, remaining_words)
        # worst case -> largest group of remaining words for a feedback combination
        worst_case = max(len(words) for words in outcomes.values())
        if worst_case < best_score:
            best_score = worst_case
            best_guess = guess
            best_outcomes = outcomes

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

def guess_word(target, bot):
    word_list = load_words_from_file('ordered_words.txt')
    remaining_words = word_list
    guess, feedback = None, None
    while guess != target:
        guess, attempt = bot.guess(feedback, guess, remaining_words)
        print(f"Bot guessed: {guess}, Attempts: {attempt}")
        feedback = generate_feedback(target, guess)
        print(f"Feedback for guess '{guess}': {feedback}")
        # update eliminated letters based on feedback
        for i in range(len(feedback)):
            if feedback[i] == 2 and guess[i] not in bot.eliminated_letters:
                if guess[i+1:].count(guess) > 1:
                    print(bot.eliminated_letters)
                    print(guess[i+1:])
                    print("adding", guess[i])
                    bot.eliminated_letters.add(guess[i])
        # filter remaining words based on new feedback
        remaining_words = filter_words(guess, feedback, remaining_words, bot.eliminated_letters)
        print(f"Remaining words after filtering: {remaining_words}")
    print("Bot guessed the correct word (", target,") in", attempt, "guesses!")
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
guess_word("words", bot)
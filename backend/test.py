from wordle_game.feedback import compute_feedback

if __name__ == "__main__":
    print(compute_feedback("abbaa", "abbey"))
    print(compute_feedback("allee", "alone"))

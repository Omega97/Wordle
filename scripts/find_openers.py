import os
from src.wordl import Wordl
from src.load_data import load_data
from src.search import Search
import numpy as np


def find_best_openers(n_iter=200_000, top_k=20, output_file="../data/best_openers.txt"):
    allowed_wordles, allowed_guesses = load_data()
    wordl = Wordl(allowed_wordles, allowed_guesses)

    # No constraints: all words are possible solutions
    # (green, yellow, black are already reset)

    n_guesses = len(wordl.guesses)
    # Initialize with one dummy visit to avoid division by zero
    prior_scores = np.full(n_guesses, 0.5)
    prior_visits = np.full(n_guesses, 1)
    search = Search(wordl, prior_values=prior_scores, prior_visits=prior_visits, c=2.0)

    print(f"Running search for best openers ({n_iter:,} iterations)...")
    for i, _ in enumerate(search.run(n_iter)):
        if (i + 1) % max(1, n_iter // 10) == 0:
            print(f"\r{i + 1:,} / {n_iter:,} iterations", end="")
    print("\nSearch complete.")

    # Compute average scores
    epsilon = 1e-8
    avg_scores = search.visits + search.values / (search.visits + epsilon)

    # Get top indices by avg score (descending)
    top_indices = np.argsort(avg_scores)[::-1][:top_k]
    top_words = [wordl.guesses[i] for i in top_indices]
    top_scores = [avg_scores[i] for i in top_indices]
    top_visits = [search.visits[i] for i in top_indices]

    # Ensure output dir exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as f:
        f.write(f"Top {top_k} Wordle openers (score = information gain, higher = better)\n")
        f.write("=" * 60 + "\n")
        for rank, (word, score, visits) in enumerate(zip(top_words, top_scores, top_visits), 1):
            f.write(f"{rank:2d}. {word.upper():>5} {score:.4f}\n")

    print(f"\nSaved top openers to: {output_file}")
    print("\nTop openers:")
    for i, word in enumerate(top_words):
        print(f"{word.upper()} {top_scores[i]:.3f}")


if __name__ == "__main__":
    find_best_openers(n_iter=500_000, top_k=1000)

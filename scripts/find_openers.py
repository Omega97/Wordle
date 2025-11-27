import os
from src.wordl import Wordl
from src.load_data import load_data
from src.search import Search
import numpy as np


def find_best_openers(n_iter, top_k=1000, output_file="../data/best_openers.txt"):
    """
    Search for the best Wordle openers, and save them in a file.
    Param:
        n_iter: number of total visits
        top_k: save this many words in the file
        output_file: output file path
    """
    # No constraints: all words are possible solutions
    # (green, yellow, black are already reset)
    allowed_wordles, allowed_guesses = load_data()
    wordl = Wordl(allowed_wordles, allowed_guesses)

    # Initialize with one dummy visit to avoid division by zero
    n_guesses = len(wordl.guesses)
    prior_scores = np.full(n_guesses, 0.5)
    prior_visits = np.full(n_guesses, 1)
    search = Search(wordl, prior_values=prior_scores, prior_visits=prior_visits, c=2.0)

    print(f"Running search for best openers ({n_iter:,} iterations)...")
    for i, _ in enumerate(search.run(n_iter)):
        if (i + 1) % max(1, n_iter // 100) == 0:
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

    # Write into the file
    with open(output_file, 'w') as f:
        for rank, (word, score, visits) in enumerate(zip(top_words, top_scores, top_visits), 1):
            f.write(f"{word.upper()}\n")

    print(f"\nSaved top openers to: {output_file}")


if __name__ == "__main__":
    find_best_openers(n_iter=300_000, top_k=1000)

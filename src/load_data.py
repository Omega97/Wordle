from pathlib import Path


# Define paths relative to the project root
BASE_DIR = Path(__file__).resolve().parent.parent  # Gets Wordl/ directory
PATHS_WORDLES = BASE_DIR / 'data' / 'shuffled_real_wordles.txt'
PATHS_GUESSES = BASE_DIR / 'data' / 'official_allowed_guesses.txt'

def load_data():
    with open(PATHS_WORDLES, encoding='utf-8') as f:
        allowed_wordles = f.read().split('\n')
        allowed_wordles = allowed_wordles[1:-1]

    with open(PATHS_GUESSES, encoding='utf-8') as f:
        allowed_guesses = f.read().split('\n')
        allowed_guesses = allowed_guesses[1:-1]

    return allowed_wordles, allowed_guesses

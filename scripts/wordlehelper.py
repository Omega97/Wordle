"""
The Interface class can help you solve a Wordle.
You can also play wordle directly with it.
"""
# todo diff crate eject evict?
# todo case insensitive rules?
from src.wordl import Wordl
from src.load_data import load_data


class WordleHelper:

    def __init__(self):
        self.allowed_wordles, self.allowed_guesses = load_data()
        self.wordl = Wordl(self.allowed_wordles, self.allowed_guesses)

    def run_helper(self, green, yellow, black, n_iter, n_display=20, c=2.):
        """
        Run the program that helps you solve any given wordle
        """
        self.wordl.set_new_colors(green, yellow, black)
        self.wordl.update_wordles()

        # Get possible solutions
        sol = self.wordl.get_possible_solutions()
        print(f'\n{len(sol)} wordles remain')
        if len(sol) < n_display:
            print(sol)
        else:
            print(sol[:n_display], '...')
        print()

        # Get best guesses
        if len(sol) == 1:
            print(f'Solution = {sol[0]}')
        else:
            self.wordl.get_best_guess(n_iter, c=c, verbose=True)

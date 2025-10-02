"""
The Interface class can help you solve a Wordle.
You can also play wordle directly with it.
"""
# todo diff crate eject evict?
from src.wordl import Wordl
from src.load_data import load_data


class Interface:

    def __init__(self):
        self.allowed_wordles, self.allowed_guesses = load_data()
        self.wordl = Wordl(self.allowed_wordles, self.allowed_guesses)

    def run_helper(self, green, yellow, black, n_iter, n_display=20):
        """
        Run the program that helps you solve any given wordle
        """
        # todo case insensitive rules
        self.wordl.set_new_colors(green, yellow, black)
        self.wordl.update_wordles()

        sol = self.wordl.get_possible_solutions()
        print(f'\n{len(sol)} wordles remain')
        if len(sol) < n_display:
            print(sol)
        else:
            print(sol[:n_display], '...')
        print()

        if len(sol) == 1:
            print(f'Solution = {sol[0]}')
        else:
            # Get best guesses
            self.wordl.get_best_guess(n_iter)

    def run_game(self):
        """
        # todo
        The program picks a random wordle, and you have to solve it.
        """
        ...

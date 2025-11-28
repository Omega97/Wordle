""" This program helps you solve today's Wordle. """
from scripts.wordlehelper import WordleHelper
from time import time
from src.color_rules import ColorRules


def main(n_iter=1_000, c=1.5):
    """
    Good starters: CRANE, SNARE, STARE, TRACE, CRATE, ...
    """
    rules = ColorRules()

    # Color rules (ADD RULES HERE)
    # rules.add_rule(guess='CRATE', code='____e')
    # rules.add_rule(guess='SOLID', code='_Ol__')

    # Run the computation
    wordle_helper = WordleHelper()
    wordle_helper.run_helper(rules.green, rules.yellow, rules.black, n_iter=n_iter, c=c)


if __name__ == '__main__':
    t = time()
    main()
    t = time() - t
    print(f'time = {t:.2f} s')

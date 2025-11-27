""" This program helps you solve today's Wordle. """
from scripts.wordlehelper import WordleHelper
from src.color_rules import ColorRules
#todo TINGE not allowed solution?


def main(n_iter=300_000, c=1.5):
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
    main()

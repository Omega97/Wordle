""" This program helps you solve today's Wordle. """
from scripts.wordlehelper import WordleHelper
from src.color_rules import ColorRules


def main(n_iter=400_000, c=2.):
    """
    Good starters: CRATE (also STANE, SHARE, TRIES)
    """
    rules = ColorRules()

    # Color rules (ADD RULES HERE)
    rules.add_rule(guess='CRATE', code = 'c___E')
    # rules.add_rule(guess='LOINS', code = 'D____')

    # Run the computation
    wordle_helper = WordleHelper()
    wordle_helper.run_helper(rules.green, rules.yellow, rules.black, n_iter=n_iter, c=c)


if __name__ == '__main__':
    main()

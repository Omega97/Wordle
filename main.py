"""
This program helps you solve the wordle.
"""
# todo add interface
from scripts.interface import Interface


class ColorRules:

    def __init__(self, word_length=5):
        self.word_length = word_length
        self.green = ['' for _ in range(word_length)]
        self.yellow = [set() for _ in range(word_length)]
        self.black = set()

    def add_rule(self, guess: str, code: str):
        """
        Convert a word and the code into colors.
        :param guess: full word
        :param code: upper case = green, lowe case = yellow, otw. black
        :return: green, yellow, black color rules

        Example:
        guess = 'CRATE'
        solution = 'QUEUE'
        code = '__e_E'
        """
        for i in range(self.word_length):
            letter = guess[i].lower()
            if code[i] == letter.upper():
                self.green[i] = letter
            elif code[i] == letter.lower():
                self.yellow[i].add(letter)
            else:
                self.black.add(letter)

    def get_rules(self):
        return self.green, self.yellow, self.black


def main():
    """
    Good starters: CRATE, STANE, SHARE, TRIES

    Good guesses:
    _____ -> lions, loins

    C____ -> ulmin, gluon
    _R___ -> pling
    __A__ -> shuln
    ___T_ -> shiny
    ____E -> loins

    c____ -> loins
    _r___ -> doily, sound
    __a__ -> sloid, solid
    ___t_ -> hoist
    ____e -> lined, solid

    __a_e -> angel
    """
    rules = ColorRules()

    # Color rules
    rules.add_rule(guess='CRATE', code = '_r__e')
    rules.add_rule(guess='SEWIN', code = '_e___')
    rules.add_rule(guess='MUCHO', code = '____o')
    rules.add_rule(guess='LORDS', code = '_or__')

    # rules.add_rule(guess='CRATE', code = 'cra__')
    # rules.add_rule(guess='CRATE', code = 'c_a_E')
    # rules.add_rule(guess='CRATE', code = '____e')
    # rules.add_rule(guess='LINED', code = 'l__E_')
    # rules.add_rule(guess='WOMBS', code = '_O___')
    # rules.add_rule(guess='HOVEL', code = 'HOVEL')

    green, yellow, black = rules.get_rules()

    interface = Interface()
    interface.run_helper(green, yellow, black,
                         n_iter=200_000, c=2.)


if __name__ == '__main__':
    main()

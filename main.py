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
    :return:
    """
    rules = ColorRules()

    # Color rules                         WIDTH
    rules.add_rule(guess='CRATE', code = '____E')
    # rules.add_rule(guess='CRATE', code = '___T_')  # shiny
    # rules.add_rule(guess='SHINY', code = '_hi__')
    # rules.add_rule(guess='FAULT', code = '____t')

    green, yellow, black = rules.get_rules()

    interface = Interface()
    interface.run_helper(green, yellow, black, n_iter=200_000)


if __name__ == '__main__':
    main()

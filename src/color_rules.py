from typing import Tuple, List, Set


class ColorRules:
    """
    Keeps track of which letters are:
    - in the correct place (green)
    - correct, but in the wrong place (yellow)
    - incorrect (black)
    """
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

    def get_green(self) -> list:
        """correct letter, correct place"""
        return self.green

    def get_yellow(self) -> list:
        """correct letter, wrong place"""
        return self.yellow

    def get_black(self) -> set:
        """wrong letter"""
        return self.black

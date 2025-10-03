import numpy as np
from copy import deepcopy
from typing import List
from src.search import Search


class Wordl:

    def __init__(self, allowed_wordles: list|tuple, allowed_guesses: list|tuple):
        assert type(allowed_wordles) in (list, tuple)
        assert type(allowed_guesses) in (list, tuple)

        self.wordles = np.array([np.array(list(s)) for s in allowed_wordles])
        self.guesses = np.array(list(set(allowed_wordles + allowed_guesses)))
        self.word_length = self.wordles.shape[1]
        self._max_score = np.log2(len(allowed_wordles))

        self.green = None   # list of letters in the right place
        self.yellow = None  # list of sets of letters in the word but not in that place
        self.black = None   # set of missing letters
        self.reset_colors()

        self.possible_solutions = None
        self.set_possible_solutions()

    def __len__(self):
        return len(self.guesses)

    def reset_colors(self):
        self.green = [''] * self.word_length
        self.yellow = [set() for _ in range(self.word_length)]
        self.black = set()

    def set_new_colors(self, green: List[str], yellow: List[set], black: set):
        """
        :param green: letter in the correct place
        :param yellow: correct letter in the wrong place
        :param black: wrong letter
        :return:
        """
        assert type(green) is list
        assert len(green) == self.word_length
        assert type(yellow) is list
        assert len(yellow) == self.word_length
        assert type(black) is set
        self.green = green
        self.yellow = yellow
        self.black = black

    def update_green(self):
        """
        Remove words that don't fit the 'green' condition
        (right letter in the right spot)
        """
        for i in range(self.word_length):
            letter = self.green[i]
            if len(letter):
                indices = self.wordles[:, i] == letter
                self.wordles = self.wordles[indices]

    def update_black(self):
        """
        Remove words that don't fit the 'black' condition
        (the given letters are not present)
        """
        for c in self.black:
            v = np.isin(self.wordles, c, assume_unique=True)
            v = np.sum(v, axis=1) == False
            self.wordles = self.wordles[v]

    def update_yellow_contains(self):
        """
        Remove words that don't fit the 'yellow' condition
        (right letter, but in the wrong spot)
        """
        for i in range(self.word_length):
            for c in self.yellow[i]:
                v = np.isin(self.wordles, c, assume_unique=True)
                v[:, i] *= False
                v = (np.sum(v, axis=1) > 0) == True
                self.wordles = self.wordles[v]

    def update_yellow_position(self):
        """
        Remove words where a yellow letter appears in the position where it was marked yellow.
        """
        for i in range(self.word_length):
            if self.yellow[i]:  # Check if the set is non-empty
                v = ~np.isin(self.wordles[:, i], list(self.yellow[i]))
                self.wordles = self.wordles[v]

    def set_possible_solutions(self):
        """Build the list of words"""
        self.possible_solutions = np.array([''.join(v) for v in self.wordles])
        if len(self.possible_solutions) == 0:
            raise ValueError('Zero possible solutions!')

    def update_wordles(self):
        """Update wordles"""
        self.update_green()
        self.update_yellow_contains()
        self.update_black()
        self.update_yellow_position()
        self.set_possible_solutions()

    def guess(self, word, solution):
        assert len(word) == self.word_length
        assert len(solution) == self.word_length
        self.reset_colors()
        for i in range(len(word)):
            if solution[i] == word[i]:
                self.green[i] = solution[i]
            else:
                if word[i] in solution:
                    self.yellow[i].add(word[i])
                else:
                    self.black.add(word[i])
        self.update_wordles()

    def get_possible_solutions(self):
        if self.possible_solutions is None:
            return self.wordles
        else:
            return self.possible_solutions

    def get_range(self):
        return len(self.wordles)

    def get_score(self):
        # x = self.get_range()
        # score = self._max_score - np.log2(x)
        # return score
        x = self.get_range()
        if x == 0:
            return 0  # No solutions remain, penalize
        if x == 1:
            return 1  # One solution, one guess needed
        return 1 / (1 + np.log2(x))  # Estimate: 1 guess + log2(x) for remaining


    def __getitem__(self, item):
        def wrap():
            word_guess = self.guesses[item]
            random_index = np.random.randint(0, len(self.wordles))
            random_solution = self.wordles[random_index]
            wordl = deepcopy(self)
            wordl.guess(word_guess, random_solution)
            wordl.update_wordles()
            return wordl.get_score()
        return wrap

    def get_best_guess(self, n_iter=50_000, c=6., n_words=5, verbose=True) -> str:
        """
        Find the word that restricts the range of solutions the most.
        Search through all allowed guesses (including allowed_wordles and allowed_guesses).
        """
        prior = self.get_score()
        if verbose:
            print(f'(prior = {prior:.2f})\n')

        search = Search(self, prior_scores=np.full(len(self.guesses), prior))

        most_common_word = None
        for i, dct in enumerate(search.run(n_iter, c=c)):
            if verbose:
                # Get top n_words indices and scores
                top_indices = np.argsort(search.scores)[-n_words:][::-1]
                top_words = [self.guesses[idx] for idx in top_indices]
                most_common_index = dct['most_visited_index']
                most_visits = dct['most_visits']
                most_common_word = self.guesses[most_common_index]
                if (i + 1) % 200 == 0:
                    txt = f'\r{i + 1:6}) '
                    if most_visits > 1:
                        words = ", ".join(top_words)
                        txt += f' top visits={most_visits:.0f}  top words: {words} '
                    print(txt, end='')

        if verbose:
            print('')

        return most_common_word

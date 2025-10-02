import numpy as np


class Search:

    def __init__(self, elements, prior_scores=None, prior_visits=None):
        """
        Find the index if the random variable with the highest
        average value in the smallest number of steps.
        Doesn't exploit correlation between the elements.

        :param elements: elements[i]() should return
            evaluation of the i-th element
        :param prior_scores: prior average score for each element
        :param prior_visits: prior number of visits for each element
        """
        self.elements = elements
        self.n_elements = len(elements)
        self.values = np.zeros(self.n_elements)  # sum of values
        self.visits = np.zeros(self.n_elements, dtype=int)
        if prior_visits is None:
            prior_visits = np.zeros(self.n_elements, dtype=int)
        if prior_visits is not None:
            self.visits += prior_visits
        if prior_scores is not None:
            self.values += prior_scores * prior_visits
        self.total_visits = 0
        self.scores = None

    def get_total_visits(self) -> int:
        return self.total_visits

    def __len__(self):
        return self.n_elements

    def get_best(self):
        """get index and value of current best element"""
        index = np.argmax(self.scores)
        value = self.scores[index]
        return index, value

    def get_best_with_prior(self):
        """Get best element """
        values = self.values + sum(self.values) / self.get_total_visits()
        visits = self.visits + 1
        scores = values / visits
        index = np.argmax(scores)
        value = scores[index]
        return index, value

    def compute_scores(self, epsilon=1e-6):
        self.scores = self.values / (self.visits + epsilon)

    def compute_priorities(self, c=2.):
        """return list of priorities given by the magic formula"""
        return self.scores + c * np.sqrt(np.log(self.get_total_visits() / self.visits))

    def get_high_priority_index(self, c=2.):
        """return index of element with the highest priority"""
        return np.argmax(self.compute_priorities(c))

    def visit(self, index):
        """get new value from high-priority
        element, then update visits and scores"""
        new_value = self.elements[index]()
        self.values[index] += new_value
        self.visits[index] += 1
        if self.scores is not None:
            self.scores[index] = self.values[index] / self.visits[index]
        self.total_visits += 1

    def get_most_visited_index(self):
        """return index and number of visits for the most visited element"""
        index = np.argmax(self.visits)
        return index, self.visits[index]

    def visit_and_get_info(self, index) -> dict:
        self.visit(index)
        if self.values is None:
            best_index, best_value = self.get_best()
        else:
            best_index, best_value = self.get_best_with_prior()
        most_visited_index, most_visits = self.get_most_visited_index()
        return {'last_visit_index': index,
                'best_index': best_index,
                'best_value': best_value,
                'most_visited_index': most_visited_index,
                'most_visits': most_visits,
                }

    def run(self, n_iter, c=2.):
        """run search
        iterating over this method yields
        a dictionary with the relevant info
        """
        n_stop = self.get_total_visits() + n_iter
        
        # Make sure every element is visited at least once
        for i in range(len(self)):
            if self.get_total_visits() >= n_stop:
                break
            if self.visits[i] == 0:
                yield self.visit_and_get_info(i)

        self.compute_scores()

        # Visit the highest priority nodes
        while True:
            if self.get_total_visits() >= n_stop:
                break
            new_index = self.get_high_priority_index(c)
            yield self.visit_and_get_info(new_index)

import numpy as np


class Search:

    def __init__(self, elements, prior_scores=None, prior_visits=None, c=2., max_visits_per_element=None):
        """
        Find the index if the random variable with the highest
        average value in the smallest number of steps.
        Doesn't exploit correlation between the elements.

        :param elements: elements[i]() should return
            evaluation of the i-th element
        :param prior_scores: prior average score for each element
        :param prior_visits: prior number of visits for each element
        :param max_visits_per_element: maximum number of visits allowed per element (None = unlimited)
        """
        self.elements = elements
        self.prior_scores = prior_scores
        self.prior_visits = prior_visits
        self.n_elements = len(elements)
        self.values = np.zeros(self.n_elements)  # sum of samples
        self.visits = np.zeros(self.n_elements, dtype=int)
        self.c = c  # Hyper-parameter
        self.max_visits_per_element = max_visits_per_element

        if prior_visits is None:
            prior_visits = np.zeros(self.n_elements, dtype=int)
        self.visits += prior_visits
        self.total_visits = self.visits.sum()

        self.priorities = None  # Which element to visit

    def get_total_visits(self) -> int:
        return self.total_visits

    def __len__(self):
        return self.n_elements

    def get_most_visited_index(self):
        """Return index of the most visited element"""
        return np.argmax(self.visits)

    def get_best_index(self):
        """Get the index of the element with the highest empirical average value"""
        if self.get_total_visits() == 0:
            return 0  # No visits yet, return first element
        scores = self.values / np.maximum(self.visits, 1)
        return np.argmax(scores)

    def get_scores(self, epsilon=1e-6):
        return self.values / (self.visits + epsilon)

    def compute_priorities(self):
        """
        Compute priorities ensuring all elements are visited at least once first.
        Respects max_visits_per_element constraint.
        """
        total = self.get_total_visits()

        # Handle max_visits constraint: find eligible elements
        if self.max_visits_per_element is not None:
            eligible_mask = (self.visits < self.max_visits_per_element)
            if not np.any(eligible_mask):
                # All elements have reached max visits - set all priorities to -inf
                self.priorities = np.full(self.n_elements, -np.inf)
                return
        else:
            eligible_mask = np.ones(self.n_elements, dtype=bool)

        # Phase 1: No visits at all - visit in order (only eligible elements)
        if total == 0:
            self.priorities = np.where(eligible_mask,
                                       np.linspace(1, 0, self.n_elements),
                                       -np.inf)
            return

        # Phase 2: Some elements still unvisited - prioritize them in order
        unvisited_mask = (self.visits == 0) & eligible_mask
        if np.any(unvisited_mask):
            unvisited_indices = np.where(unvisited_mask)[0]
            unvisited_priorities = np.full(self.n_elements, -np.inf)

            # Assign decreasing priorities to unvisited elements to visit in order
            for i, idx in enumerate(unvisited_indices):
                unvisited_priorities[idx] = len(unvisited_indices) - i

            self.priorities = unvisited_priorities
            return

        # Phase 3: All elements visited - use standard UCB (only for eligible elements)
        scores = self.values / self.visits
        exploration = self.c * np.sqrt(np.log(total) / self.visits)
        ucb_priorities = scores + exploration

        # Set ineligible elements to -inf so they won't be selected
        self.priorities = np.where(eligible_mask, ucb_priorities, -np.inf)

    def get_priorities(self) -> np.array:
        """Get priorities (compute priorities if needed)"""
        if self.priorities is None:
            self.compute_priorities()
        return self.priorities

    def get_high_priority_index(self):
        """return index of element with the highest priority"""
        priorities = self.get_priorities()
        if np.all(priorities == -np.inf):
            # No eligible elements - return first element (though visit will be skipped)
            return 0
        return np.argmax(priorities)

    def visit(self, index):
        """Get new value from high-priority element, then update visits and scores"""
        # Check if we can still visit this element
        if (self.max_visits_per_element is not None and
                self.visits[index] >= self.max_visits_per_element):
            # Skip visiting - just return without updating
            return

        # Get the new sample
        new_value = self.elements[index]()

        # Update values and visits
        self.values[index] += new_value
        self.visits[index] += 1
        self.total_visits += 1

        # Set priorities to be recomputed
        self.priorities = None

    def _get_info(self, index):
        best_index = self.get_best_index()
        most_visited_index = self.get_most_visited_index()
        # Return average value for best element, not sum
        best_value = self.values[best_index] / max(self.visits[best_index], 1)
        return {'last_visit_index': index,
                'best_index': best_index,
                'best_value': best_value,
                'most_visited_index': most_visited_index,
                'most_visits': self.visits[most_visited_index],
                }

    def visit_and_get_info(self, index) -> dict:
        self.visit(index)
        return self._get_info(index)

    def _visit_high_priority_elements(self, n_stop):
        """Visit the highest priority nodes.

        Yields dictionaries with relevant info for each visit.
        Stops early if all elements reach max_visits_per_element.
        """
        while self.get_total_visits() < n_stop:
            new_index = self.get_high_priority_index()

            # Check if we can actually visit this element
            if (self.max_visits_per_element is not None and
                    self.visits[new_index] >= self.max_visits_per_element):
                # All elements have reached max visits - halt
                break

            yield self.visit_and_get_info(new_index)

    def run(self, n_iter):
        """Run search.

        Iterating over this method yields a dictionary with the relevant info.
        """
        n_stop = self.get_total_visits() + n_iter

        # Visit the highest priority nodes
        yield from self._visit_high_priority_elements(n_stop)

import numpy as np
import matplotlib.pyplot as plt
from src.search import Search


def test_search(n_elements=15, n_iter=300, noise=0.4, c=2.):
    np.random.seed(1)

    # to save evaluations for the plot
    values = [[] for _ in range(n_elements)]

    # define elements to explore
    def element(index):
        """evaluate a fictitious element of a certain index"""
        def wrap():
            value = index / (n_elements - 1) + np.random.normal() * noise
            values[index].append(value)
            return value
        return wrap

    elements = [element(i) for i in range(n_elements)]

    # run search
    search = Search(elements, c=c)
    count = np.zeros(n_elements)
    visits = np.zeros(n_elements)
    search_iter = search.run(n_iter=n_iter)

    # take track of visits (*optional)
    for i, dct in enumerate(search_iter):
        count[dct["best_index"]] += 1
        visits[dct["last_visit_index"]] += 1

    # plot (*optional)
    fig, ax = plt.subplots(nrows=3)
    plt.suptitle(f'Example of an exploration-exploitation scenario')

    plt.sca(ax[0])
    plt.title(' #times voted as best', loc='left', pad=-14, y=1.)
    plt.bar(list(range(1, 1 + n_elements)), count, width=1)
    plt.xticks(list(range(1, 1 + n_elements)))

    plt.sca(ax[1])
    plt.title(' #times visited', loc='left', pad=-14, y=1.)
    plt.bar(list(range(1, 1 + n_elements)), visits, width=1, color='r')
    plt.xticks(list(range(1, 1 + n_elements)))

    plt.sca(ax[2])
    plt.title(' values', loc='left', pad=-14, y=1.)
    for i in range(n_elements):
        plt.scatter(np.ones(len(values[i])) * i+1, values[i], color='k', alpha=.3)
    plt.xlim(0, n_elements+1)
    plt.xticks(list(range(1, 1 + n_elements)))

    plt.show()


if __name__ == '__main__':
    test_search()

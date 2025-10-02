from src.load_data import PATHS_WORDLES, PATHS_GUESSES


def test_1():
    wordles = open(PATHS_WORDLES).read().splitlines()
    print()
    for w in wordles:
        if 'c' in w and 't' in w and w[1] == 'i':
            print(w)


def test_2():
    wordles = open(PATHS_GUESSES).read().splitlines()
    print()
    for w in wordles:
        if 'c' in w and 't' in w and w[1] == 'i':
            print(w)


if __name__ == '__main__':
    test_1()
    test_2()

import copy
import random
from CreateMatrix import createMatrix, createMatrix_wrap
from ReadInput import readFile, readTerminal
from Algorithms.Greedy_unwrap import Greedy
from Algorithms.DFS_unwrap import DFS
from Algorithms.Greedy_wrap import Greedy_wrap
from Algorithms.DFS_wrap import DFS_wrap

import time

def test(number_testcase, size_begin, size_end, name):
    print("Welcome to", name)
    for n in range(size_begin, size_end+1):
        total = 0
        for seed in range(0, number_testcase):
            random.seed(seed)
            if name == "DFS":
                 matrix = createMatrix(n)
                 algorithm = DFS(n, matrix)
            elif name == "DFS_wrap":
                 matrix = createMatrix_wrap(n)
                 algorithm = DFS_wrap(n, matrix)
            elif name == "Greedy":
                 matrix = createMatrix(n)
                 algorithm = Greedy(n, matrix)
            else:
                 matrix = createMatrix_wrap(n)
                 algorithm = Greedy_wrap(n, matrix)

            start = time.time()
            ans = algorithm.solve()
            end = time.time()

            total += end - start
            if ans == 0:
                print("DFS can't solve")

        print("Size:", n, ":", total / number_testcase)


if __name__ == "__main__":

    #test(100, 4, 20, "DFS")

    #test(100, 4, 20, "Greedy")
    #test(100, 21, 25, "Greedy")

    test(100, 4, 15, "DFS_wrap")

    test(100, 4, 15, "Greedy_wrap")
    test(100, 16, 20, "Greedy_wrap")



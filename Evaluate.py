import copy
import random
from CreateMatrix import createMatrix, createMatrix_wrap
from ReadInput import readFile, readTerminal
from Algorithms.Greedy_unwrap import Greedy
from Algorithms.DFS_unwrap import DFS
from Algorithms.Greedy_wrap import Greedy_wrap
from Algorithms.DFS_wrap import DFS_wrap
import tracemalloc
import numpy as np

import time

def format_memory(size_mib):
    """Convert memory size from MiB to the most suitable unit."""
    size_bytes = size_mib * 1024 * 1024  # Convert MiB to Bytes
    
    if size_bytes < 1024:
        return f"{size_bytes:.2f} Bytes"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KiB"
    else:
        return f"{size_mib:.2f} MiB"

def memory_usage_test(number_testcase, size_begin, size_end, name):
    print("Welcome to", name)
    for n in range(size_begin, size_end+1):
        memories = []
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
            tracemalloc.start()
            ans = algorithm.solve()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop() 
            memories.append(peak / 1024)
            if ans == 0:
                print("DFS can't solve")

        avg_memory = np.mean(memories)
        std_memory = np.std(memories)

        print("Size", n, ":")
        print(f"Average memory usage: {avg_memory} KiB (+/- {std_memory})")

def execution_time_test(number_testcase, size_begin, size_end, name):
    print("Welcome to", name)
    for n in range(size_begin, size_end+1):
        times = []
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

            start_time  = time.time()
            ans = algorithm.solve()
            end_time  = time.time()

            times.append(end_time - start_time)
            if ans == 0:
                print("DFS can't solve")

        avg_time = np.mean(times)
        std_time = np.std(times)

        print("Size", n, ":")
        print(f"Average execution time: {avg_time:.6f} seconds (+/- {std_time:.6f})")

if __name__ == "__main__":

    execution_time_test(50, 4, 20, "DFS")

    execution_time_test(50, 4 , 20, "Greedy")

    execution_time_test(50, 4, 12, "DFS_wrap")

    execution_time_test(50, 4, 20, "Greedy_wrap")
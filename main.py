import copy
import random
from xml.dom.minidom import Element
from CreateMatrix import createMatrix, createMatrix_wrap
from ReadInput import readFile, readTerminal
from Algorithms.Greedy_unwrap import Greedy
from Algorithms.DFS_unwrap import DFS
from Algorithms.Greedy_wrap import Greedy_wrap
from Algorithms.DFS_wrap import DFS_wrap
from Visualizer.PipeVisualizer import PipeVisualizer, Pipe, PipeType, Grid

if __name__ == "__main__":
    case1 = -2

    while case1 != -1:    
        print("Which algorithm would you like to test?")
        print("-1: Exit")
        print("0: DFS with an unwrapped puzzle")
        print("1: Greedy with an unwrapped puzzle")
        print("2: DFS with a wrap puzzle")
        print("3: Greedy with a wrap puzzle")
        case1 = int(input("Your choice: "))

        if case1 == -1:
            break

        print("----------------------------")
        print("How do you input the puzzle?")
        print("-1: Go back")
        print("0: From a .txt file")
        print("1: Enter manually in the terminal")
        print("2+: Generate randomly using a seed")
        case2 = int(input("Your choice: "))

        if case2 == -1:
            print("----------------------------")
            continue
        elif case2 == 0:
            n, matrix = readFile("Input_Matrix.txt")
        elif case2 == 1:
            n, matrix = readTerminal()
        else:
            random.seed(case2)

            case3 = int(input("Size: "))
            n = case3
            if case1 == 0 or case1 == 1:
                matrix = createMatrix(case3)
            else:
                matrix = createMatrix_wrap(case3)
            print(n)
            for row in matrix:
                for ele in row:
                    print(ele, end = " ")
                print()

        print("----------------------------")
        print("Do you need visualization?")
        print("-1: Go back")
        print("0: Step-by-step visualization")
        print("1: Show only the final answer")
        print("2: Text output only")
        case4 = int(input("Your choice: "))
        
        if case4 == -1:
            print("----------------------------")
            continue
        elif case4 == 0:
            visualizer = PipeVisualizer(750 // n)
            if case1 == 0:
                visualizer.visualize_solution(n, matrix, "DFS_unwrap")
            elif case1 == 1:
                visualizer.visualize_solution(n, matrix, "Greedy_unwrap")
            elif case1 == 2:
                visualizer.visualize_solution(n, matrix, "DFS_wrap")
            else:
                visualizer.visualize_solution(n, matrix, "Greedy_wrap")
        else:
            if case1 == 0:
                algorithm = DFS(n, matrix)
            elif case1 == 1:
                algorithm = Greedy(n, matrix)
            elif case1 == 2:
                algorithm = DFS_wrap(n, matrix)
            else:
                algorithm = Greedy_wrap(n, matrix)
            ans = algorithm.solve()
            if ans == 0:
                print("----------------------------")
                print("Can't solve")
                _ = input("Press anything to continue")
                print("----------------------------")
            
            if case4 == 1:
                visualizer = PipeVisualizer(750 // n)
                if case1 == 0 or case1 == 1:
                    visualizer.visualize(n, matrix, ans)
                else:
                    visualizer.visualize(n, matrix, ans, wrap_able=True)
            else:
                for row in ans:
                    print(row)
                print("----------------------------")
                _ = input("Press anything to continue")
                print("----------------------------")



        
    


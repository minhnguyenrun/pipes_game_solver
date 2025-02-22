# Read information from Input_Matrix.txt
def readFile(filename):
    with open(filename, 'r') as file:
        n = int(file.readline().strip())
        
        matrix = []
        for _ in range(n):
            row = list(map(int, file.readline().strip().split()))
            matrix.append(row)
    
    return n, matrix

def readTerminal():
    n = int(input())

    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    return n, matrix
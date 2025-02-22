import random

def createMatrix(n):
    #
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    ans_matrix = [["" for _ in range(n)] for _ in range(n)]
    queue = []
    queue.append((n // 2, n // 2))
    options = [(1, "U"), 
                (1, "D"), 
                (1, "L"), 
                (1, "R"), 
                (2, "UD"), 
                (2, "RL"), 
                (3, "UL"), 
                (3, "UR"), 
                (3, "DL"), 
                (3, "DR"), 
                (4, "UDL"), 
                (4, "UDR"), 
                (4, "DRL"), 
                (4, "URL"), 
                ]
    correct = 0
    while correct == 0:
        while queue:
            i, j = queue.pop(0)
            available_options = []
        
            for option in options:
                rotation = option[1]
                ok = 1
                if 'U' in rotation:
                    if ((i - 1, j) in queue) or i == 0 or not (ans_matrix[i - 1][j] == "" or 'D' in ans_matrix[i - 1][j]):
                        continue
                else:
                    if i != 0 and 'D' in ans_matrix[i - 1][j]:
                        continue

                if 'D' in rotation:
                    if ((i + 1, j) in queue) or i == n - 1 or not (ans_matrix[i + 1][j] == "" or 'U' in ans_matrix[i + 1][j]):
                        continue
                else:
                    if i != n - 1 and 'U' in ans_matrix[i + 1][j]:
                        continue

                if 'L' in rotation:
                    if ((i, j - 1) in queue) or j == 0 or not (ans_matrix[i][j - 1] == "" or 'R' in ans_matrix[i][j - 1]):
                        continue
                else:
                    if j != 0 and 'R' in ans_matrix[i][j - 1]:
                        continue

                if 'R' in rotation:
                    if ((i, j + 1) in queue) or j == n - 1 or not (ans_matrix[i][j + 1] == "" or 'L' in ans_matrix[i][j + 1]):
                        continue
                else:
                    if j != n - 1 and 'L' in ans_matrix[i][j + 1]:
                        continue
                available_options.append(option)

            if not available_options:
                continue

            choose = random.randint(0, len(available_options) - 1)
            matrix[i][j] = available_options[choose][0]
            ans_matrix[i][j] = available_options[choose][1]

            rotation = available_options[choose][1]
            for direction in rotation:
                if direction == 'U':
                    if i != 0 and ans_matrix[i - 1][j] == "":
                        queue.append((i - 1, j))
                elif direction == 'D':
                    if i != n - 1 and ans_matrix[i + 1][j] == "":
                        queue.append((i + 1, j))
                elif direction == 'L':
                    if j != 0 and ans_matrix[i][j - 1] == "":
                        queue.append((i, j - 1))
                else:
                    if j != n - 1 and ans_matrix[i][j + 1] == "":
                        queue.append((i, j + 1))

        correct = 1
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 0:
                    if i != 0 and matrix[i - 1][j] != 4 and matrix[i - 1][j] != 0:
                        ans_matrix[i - 1][j] += "D"
                        if len(ans_matrix[i - 1][j]) == 3:
                            matrix[i - 1][j] = 4
                        elif 'U' in ans_matrix[i - 1][j]:
                            matrix[i - 1][j] = 2
                        else:
                            matrix[i - 1][j] = 3
                        correct = 0
                        queue.append((i, j))
                        break
                    if i != n - 1 and matrix[i + 1][j] != 4 and matrix[i + 1][j] != 0: 
                        ans_matrix[i + 1][j] += "U"
                        if len(ans_matrix[i + 1][j]) == 3:
                            matrix[i + 1][j] = 4
                        elif 'D' in ans_matrix[i + 1][j]:
                            matrix[i + 1][j] = 2
                        else:
                            matrix[i + 1][j] = 3
                        correct = 0
                        queue.append((i, j))
                        break
                    if j != 0 and matrix[i][j - 1] != 4 and matrix[i][j - 1] != 0:
                        ans_matrix[i][j - 1] += "R"
                        if len(ans_matrix[i][j - 1]) == 3:
                            matrix[i][j - 1] = 4
                        elif 'L' in ans_matrix[i][j - 1]:
                            matrix[i][j - 1] = 2
                        else:
                            matrix[i][j - 1] = 3
                        correct = 0
                        queue.append((i, j))
                        break
                    if j != n - 1 and matrix[i][j + 1] != 4 and matrix[i][j + 1] != 0:
                        ans_matrix[i][j + 1] += "L"
                        if len(ans_matrix[i][j + 1]) == 3:
                            matrix[i][j + 1] = 4
                        elif 'R' in ans_matrix[i][j + 1]:
                            matrix[i][j + 1] = 2
                        else:
                            matrix[i][j + 1] = 3
                        correct = 0
                        queue.append((i, j))
                        break



            if correct == 0:
                break
    #for row in ans_matrix:
    #    print(row)
    return matrix


def createMatrix_wrap(n):
    #
    matrix = [[0 for _ in range(n)] for _ in range(n)]
    ans_matrix = [["" for _ in range(n)] for _ in range(n)]
    queue = []
    queue.append((n // 2, n // 2))
    options = [(1, "U"), 
                (1, "D"), 
                (1, "L"), 
                (1, "R"), 
                (2, "UD"), 
                (2, "RL"), 
                (3, "UL"), 
                (3, "UR"), 
                (3, "DL"), 
                (3, "DR"), 
                (4, "UDL"), 
                (4, "UDR"), 
                (4, "DRL"), 
                (4, "URL"), 
                ]
    correct = 0
    while correct == 0:
        while queue:
            i, j = queue.pop(0)
            available_options = []

            UP = (i - 1, j)
            DOWN = (i + 1, j)
            LEFT = (i, j - 1)
            RIGHT = (i, j + 1)
            if UP[0] == -1: UP = (n - 1, j)
            if DOWN[0] == n: DOWN = (0, j)
            if LEFT[1] == -1: LEFT = (i, n - 1)
            if RIGHT[1] == n: RIGHT = (i, 0)

            ans_matrix[UP[0]][UP[1]] = ans_matrix[UP[0]][UP[1]]
            ans_matrix[DOWN[0]][DOWN[1]] = ans_matrix[DOWN[0]][DOWN[1]]
            ans_matrix[RIGHT[0]][RIGHT[1]] = ans_matrix[RIGHT[0]][RIGHT[1]]
            ans_matrix[LEFT[0]][LEFT[1]] = ans_matrix[LEFT[0]][LEFT[1]]

            for option in options:
                rotation = option[1]
                ok = 1
                if 'U' in rotation:
                    if (UP in queue) or not (ans_matrix[UP[0]][UP[1]] == "" or 'D' in ans_matrix[UP[0]][UP[1]]):
                        continue
                else:
                    if 'D' in ans_matrix[UP[0]][UP[1]]:
                        continue

                if 'D' in rotation:
                    if (DOWN in queue) or not (ans_matrix[DOWN[0]][DOWN[1]] == "" or 'U' in ans_matrix[DOWN[0]][DOWN[1]]):
                        continue
                else:
                    if 'U' in ans_matrix[DOWN[0]][DOWN[1]]:
                        continue

                if 'L' in rotation:
                    if (LEFT in queue) or not (ans_matrix[LEFT[0]][LEFT[1]] == "" or 'R' in ans_matrix[LEFT[0]][LEFT[1]]):
                        continue
                else:
                    if 'R' in ans_matrix[LEFT[0]][LEFT[1]]:
                        continue

                if 'R' in rotation:
                    if (RIGHT in queue) or not (ans_matrix[RIGHT[0]][RIGHT[1]] == "" or 'L' in ans_matrix[RIGHT[0]][RIGHT[1]]):
                        continue
                else:
                    if 'L' in ans_matrix[RIGHT[0]][RIGHT[1]]:
                        continue

                available_options.append(option)

            if not available_options:
                continue

            choose = random.randint(0, len(available_options) - 1)
            matrix[i][j] = available_options[choose][0]
            ans_matrix[i][j] = available_options[choose][1]

            #for row in ans_matrix:
            #    print(row)
            #print("---")

            rotation = available_options[choose][1]
            for direction in rotation:
                if direction == 'U':
                    if ans_matrix[UP[0]][UP[1]] == "":
                        queue.append(UP)
                elif direction == 'D':
                    if ans_matrix[DOWN[0]][DOWN[1]] == "":
                        queue.append(DOWN)
                elif direction == 'L':
                    if ans_matrix[LEFT[0]][LEFT[1]] == "":
                        queue.append(LEFT)
                else:
                    if ans_matrix[RIGHT[0]][RIGHT[1]] == "":
                        queue.append(RIGHT)

        correct = 1
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 0:
                    UP = (i - 1, j)
                    DOWN = (i + 1, j)
                    LEFT = (i, j - 1)
                    RIGHT = (i, j + 1)
                    if UP[0] == -1: UP = (n - 1, j)
                    if DOWN[0] == n: DOWN = (0, j)
                    if LEFT[1] == -1: LEFT = (i, n - 1)
                    if RIGHT[1] == n: RIGHT = (i, 0)



                    if matrix[UP[0]][UP[1]] != 4 and matrix[UP[0]][UP[1]] != 0:
                        ans_matrix[UP[0]][UP[1]] += "D"
                        if len(ans_matrix[UP[0]][UP[1]]) == 3:
                            matrix[UP[0]][UP[1]] = 4
                        elif 'U' in ans_matrix[UP[0]][UP[1]]:
                            matrix[UP[0]][UP[1]] = 2
                        else:
                            matrix[UP[0]][UP[1]] = 3
                        correct = 0
                        queue.append((i, j))
                        break
                    if matrix[DOWN[0]][DOWN[1]] != 4 and matrix[DOWN[0]][DOWN[1]] != 0: 
                        ans_matrix[DOWN[0]][DOWN[1]] += "U"
                        if len(ans_matrix[DOWN[0]][DOWN[1]]) == 3:
                            matrix[DOWN[0]][DOWN[1]] = 4
                        elif 'D' in ans_matrix[DOWN[0]][DOWN[1]]:
                            matrix[DOWN[0]][DOWN[1]] = 2
                        else:
                            matrix[DOWN[0]][DOWN[1]] = 3
                        correct = 0
                        queue.append((i, j))
                        break
                    if matrix[LEFT[0]][LEFT[1]] != 4 and matrix[LEFT[0]][LEFT[1]] != 0:
                        ans_matrix[LEFT[0]][LEFT[1]] += "R"
                        if len(ans_matrix[LEFT[0]][LEFT[1]]) == 3:
                            matrix[LEFT[0]][LEFT[1]] = 4
                        elif 'L' in ans_matrix[LEFT[0]][LEFT[1]]:
                            matrix[LEFT[0]][LEFT[1]] = 2
                        else:
                            matrix[LEFT[0]][LEFT[1]] = 3
                        correct = 0
                        queue.append((i, j))
                        break
                    if matrix[RIGHT[0]][RIGHT[1]] != 4 and matrix[RIGHT[0]][RIGHT[1]] != 0:
                        ans_matrix[RIGHT[0]][RIGHT[1]] += "L"
                        if len(ans_matrix[RIGHT[0]][RIGHT[1]]) == 3:
                            matrix[RIGHT[0]][RIGHT[1]] = 4
                        elif 'R' in ans_matrix[RIGHT[0]][RIGHT[1]]:
                            matrix[RIGHT[0]][RIGHT[1]] = 2
                        else:
                            matrix[RIGHT[0]][RIGHT[1]] = 3
                        correct = 0
                        queue.append((i, j))
                        break



            if correct == 0:
                break

    #for row in ans_matrix:
    #    print(row)
    return matrix


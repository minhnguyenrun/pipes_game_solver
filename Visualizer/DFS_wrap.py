import copy
from collections import deque

class DFS_wrap:
    def __init__(self, n, matrix):
        self.n = n
        self.target_score = n * n
        self.matrix = matrix
        self.visualizer = []

    def checkRotation(self, i, j, rotate):
        if 'U' in rotate:
            if (i != 0 and not (self.rotation_matrix[i - 1][j] == "" or 'D' in self.rotation_matrix[i - 1][j])) or (i == 0 and not (self.rotation_matrix[self.n - 1][j] == "" or 'D' in self.rotation_matrix[self.n - 1][j])):
                return 0
        else:
            if (i != 0 and 'D' in self.rotation_matrix[i - 1][j]) or (i == 0 and 'D' in self.rotation_matrix[self.n - 1][j]):
                return 0

        if 'D' in rotate:
            if (i != self.n - 1 and not (self.rotation_matrix[i + 1][j] == "" or 'U' in self.rotation_matrix[i + 1][j])) or (i == self.n - 1 and not (self.rotation_matrix[0][j] == "" or 'U' in self.rotation_matrix[0][j])):
                return 0
        else:
            if (i != self.n - 1 and 'U' in self.rotation_matrix[i + 1][j]) or (i == self.n - 1 and 'U' in self.rotation_matrix[0][j]):
                return 0

        if 'L' in rotate:
            if (j != 0 and not (self.rotation_matrix[i][j - 1] == "" or 'R' in self.rotation_matrix[i][j - 1])) or (j == 0 and not (self.rotation_matrix[i][self.n - 1] == "" or 'R' in self.rotation_matrix[i][self.n - 1])):
                return 0
        else:
            if (j != 0 and 'R' in self.rotation_matrix[i][j - 1]) or (j == 0 and 'R' in self.rotation_matrix[i][self.n - 1]):
                return 0

        if 'R' in rotate:
            if (j != self.n - 1 and not (self.rotation_matrix[i][j + 1] == "" or 'L' in self.rotation_matrix[i][j + 1])) or (j == self.n - 1 and not (self.rotation_matrix[i][0] == "" or 'L' in self.rotation_matrix[i][0])):
                return 0
        else:
            if (j != self.n - 1 and 'L' in self.rotation_matrix[i][j + 1]) or (j == self.n - 1 and 'L' in self.rotation_matrix[i][0]):
                return 0

        return 1

    def deepChecker(self):
        color = [[0 for _ in range(self.n)] for _ in range(self.n)]
        queue = deque()
        queue.append((self.n // 2, self.n // 2))
        score = 0
        while queue:
            i, j = queue.popleft()
            if color[i][j] == 1:
                continue
            for direction in self.rotation_matrix[i][j]:
                if direction == 'U':
                    UP = i - 1 if i != 0 else self.n - 1
                    if self.rotation_matrix[UP][j] != None and 'D' in self.rotation_matrix[UP][j]: queue.append((UP, j))
                elif direction == 'D':
                    DOWN = i + 1 if i != self.n - 1 else 0
                    if self.rotation_matrix[DOWN][j] != None and 'U' in self.rotation_matrix[DOWN][j]: queue.append((DOWN, j))
                elif direction == 'L':
                    LEFT = j - 1 if j != 0 else self.n - 1
                    if self.rotation_matrix[i][LEFT] != None and 'R' in self.rotation_matrix[i][LEFT]: queue.append((i, LEFT))
                elif direction == 'R':
                    RIGHT = j + 1 if j != self.n - 1 else 0
                    if self.rotation_matrix[i][RIGHT] != None and 'L' in self.rotation_matrix[i][RIGHT]: queue.append((i, RIGHT))
            color[i][j] = 1
            score += 1
        if score == self.target_score:
            return self.rotation_matrix
        return 0


    def findRotation(self, i, j):
        pipe_type = self.matrix[i][j]
        rotation_list = []
        if pipe_type == 1:
            if self.checkRotation(i, j, "U"):
                rotation_list.append("U")
            if self.checkRotation(i, j, "L"):
                rotation_list.append("L")
            if self.checkRotation(i, j, "D"):
                rotation_list.append("D")
            if self.checkRotation(i, j, "R"):
                rotation_list.append("R")

            if rotation_list:
                more_checker = []
                for rotate in rotation_list:
                    if rotate == 'U':
                        if (i != 0 and self.matrix[i - 1][j] == 1) or (i == 0 and self.matrix[self.n - 1][j] == 1):
                            continue
                    elif rotate == 'D':
                        if (i != self.n - 1 and self.matrix[i + 1][j] == 1) or (i == self.n - 1 and self.matrix[0][j] == 1):
                            continue
                    elif rotate == 'L':
                        if (j != 0 and self.matrix[i][j - 1] == 1) or (j == 0 and self.matrix[i][self.n - 1] == 1):
                            continue
                    else:
                        if (j != self.n - 1 and self.matrix[i][j + 1] == 1) or (j == self.n - 1 and self.matrix[i][0] == 1):
                            continue
                    more_checker.append(rotate)
                rotation_list = more_checker

        elif pipe_type == 2:
            if self.checkRotation(i, j, "UD"):
                rotation_list.append("UD")
            if self.checkRotation(i, j, "LR"):
                rotation_list.append("LR")
        elif pipe_type == 3:
            if self.checkRotation(i, j, "UL"):
                rotation_list.append("UL")
            if self.checkRotation(i, j, "DL"):
                rotation_list.append("DL")
            if self.checkRotation(i, j, "UR"):
                rotation_list.append("UR")
            if self.checkRotation(i, j, "DR"):
                rotation_list.append("DR")
        else:
            if self.checkRotation(i, j, "UDL"):
                rotation_list.append("UDL")
            if self.checkRotation(i, j, "UDR"):
                rotation_list.append("UDR")
            if self.checkRotation(i, j, "URL"):
                rotation_list.append("URL")
            if self.checkRotation(i, j, "DRL"):
                rotation_list.append("DRL")
        return rotation_list

    def solve(self):
        self.rotation_matrix = [["" for _ in range(self.n)] for _ in range(self.n)]
        return self.findState(0, 0)

    def findState(self, i, j):

        rotation_list = self.findRotation(i, j)

        next_i = i if j != self.n - 1 else i + 1
        next_j = j + 1 if j != self.n - 1 else 0

        for rotation in rotation_list:
            self.rotation_matrix[i][j] = rotation
            self.visualizer.append(copy.deepcopy(self.rotation_matrix))
            if i == self.n - 1 and j == self.n - 1:
                ans = self.deepChecker()
                if ans != 0:
                    return ans
                self.rotation_matrix[i][j] = ""
                return 0
            ans = self.findState(next_i, next_j)
            if ans != 0:
                return ans

        self.rotation_matrix[i][j] = ""

        return 0
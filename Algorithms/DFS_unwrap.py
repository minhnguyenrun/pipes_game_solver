import copy
import queue
from collections import deque

import sys
sys.setrecursionlimit(2000)

class DFS:
    def __init__(self, n, matrix):
        self.n = n
        self.target_score = n * n
        self.matrix = matrix

    def deepChecker(self):
        if self.rotation_matrix[self.n // 2][self.n // 2] == "":
            return 1
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
                    if i != 0 and self.rotation_matrix[i - 1][j] != "" and 'D' in self.rotation_matrix[i - 1][j]:
                        queue.append((i - 1, j))
                    else:
                        return 1
                elif direction == 'D':
                    if i != self.n - 1 and self.rotation_matrix[i + 1][j] != "" and 'U' in self.rotation_matrix[i + 1][j]:
                        queue.append((i + 1, j))
                    else:
                        return 1
                elif direction == 'L':
                    if j != 0 and self.rotation_matrix[i][j - 1] != "" and 'R' in self.rotation_matrix[i][j - 1]:
                        queue.append((i, j - 1))
                    else:
                        return 1
                elif direction == 'R':
                    if j != self.n - 1 and self.rotation_matrix[i][j + 1] != "" and 'L' in self.rotation_matrix[i][j + 1]:
                        queue.append((i, j + 1))
                    else:
                        return 1
            color[i][j] = 1
            score += 1
        if score == self.target_score:
            return self.rotation_matrix
        return 0

    def checkRotation(self, i, j, rotation):
        if 'U' in rotation:
            if i == 0 or not (self.rotation_matrix[i - 1][j] == "" or 'D' in self.rotation_matrix[i - 1][j]):
                return 0
        else:
            if i != 0 and 'D' in self.rotation_matrix[i - 1][j]:
                return 0

        if 'D' in rotation:
            if i == self.n - 1 or not (self.rotation_matrix[i + 1][j] == "" or 'U' in self.rotation_matrix[i + 1][j]):
                return 0
        else:
            if i != self.n - 1 and 'U' in self.rotation_matrix[i + 1][j]:
                return 0

        if 'L' in rotation:
            if j == 0 or not (self.rotation_matrix[i][j - 1] == "" or 'R' in self.rotation_matrix[i][j - 1]):
                return 0
        else:
            if j != 0 and 'R' in self.rotation_matrix[i][j - 1]:
                return 0

        if 'R' in rotation:
            if j == self.n - 1 or not (self.rotation_matrix[i][j + 1] == "" or 'L' in self.rotation_matrix[i][j + 1]):
                return 0
        else:
            if j != self.n - 1 and 'L' in self.rotation_matrix[i][j + 1]:
                return 0

        return 1

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
                advance_checker = []
                for rotate in rotation_list:
                    if rotate == 'U':
                        if self.matrix[i - 1][j] == 1:
                            continue
                    elif rotate == 'D':
                        if self.matrix[i + 1][j] == 1:
                            continue
                    elif rotate == 'L':
                        if self.matrix[i][j - 1] == 1:
                            continue
                    else:
                        if self.matrix[i][j + 1] == 1:
                            continue
                    advance_checker.append(rotate)
                rotation_list = advance_checker

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

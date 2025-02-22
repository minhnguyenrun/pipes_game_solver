import copy

class DFS_wrap:
    def __init__(self, n, matrix):
        self.n = n
        self.target_score = n * n
        self.matrix = matrix
        self.visualizer = []

    def checkRotation(self, i, j, rotate, rotation_matrix):
        if 'U' in rotate:
            if (i != 0 and not (rotation_matrix[i - 1][j] == "" or 'D' in rotation_matrix[i - 1][j])) or (i == 0 and not (rotation_matrix[self.n - 1][j] == "" or 'D' in rotation_matrix[self.n - 1][j])):
                return 0
        else:
            if (i != 0 and 'D' in rotation_matrix[i - 1][j]) or (i == 0 and 'D' in rotation_matrix[self.n - 1][j]):
                return 0

        if 'D' in rotate:
            if (i != self.n - 1 and not (rotation_matrix[i + 1][j] == "" or 'U' in rotation_matrix[i + 1][j])) or (i == self.n - 1 and not (rotation_matrix[0][j] == "" or 'U' in rotation_matrix[0][j])):
                return 0
        else:
            if (i != self.n - 1 and 'U' in rotation_matrix[i + 1][j]) or (i == self.n - 1 and 'U' in rotation_matrix[0][j]):
                return 0

        if 'L' in rotate:
            if (j != 0 and not (rotation_matrix[i][j - 1] == "" or 'R' in rotation_matrix[i][j - 1])) or (j == 0 and not (rotation_matrix[i][self.n - 1] == "" or 'R' in rotation_matrix[i][self.n - 1])):
                return 0
        else:
            if (j != 0 and 'R' in rotation_matrix[i][j - 1]) or (j == 0 and 'R' in rotation_matrix[i][self.n - 1]):
                return 0

        if 'R' in rotate:
            if (j != self.n - 1 and not (rotation_matrix[i][j + 1] == "" or 'L' in rotation_matrix[i][j + 1])) or (j == self.n - 1 and not (rotation_matrix[i][0] == "" or 'L' in rotation_matrix[i][0])):
                return 0
        else:
            if (j != self.n - 1 and 'L' in rotation_matrix[i][j + 1]) or (j == 0 and 'L' in rotation_matrix[i][0]):
                return 0

        return 1


    def findRotation(self, i, j, rotation_matrix):
        pipe_type = self.matrix[i][j]
        rotation_list = []
        if pipe_type == 1:
            if self.checkRotation(i, j, "U", rotation_matrix):
                rotation_list.append("U")
            if self.checkRotation(i, j, "L", rotation_matrix):
                rotation_list.append("L")
            if self.checkRotation(i, j, "D", rotation_matrix):
                rotation_list.append("D")
            if self.checkRotation(i, j, "R", rotation_matrix):
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
            if self.checkRotation(i, j, "UD", rotation_matrix):
                rotation_list.append("UD")
            if self.checkRotation(i, j, "LR", rotation_matrix):
                rotation_list.append("LR")
        elif pipe_type == 3:
            if self.checkRotation(i, j, "UL", rotation_matrix):
                rotation_list.append("UL")
            if self.checkRotation(i, j, "DL", rotation_matrix):
                rotation_list.append("DL")
            if self.checkRotation(i, j, "UR", rotation_matrix):
                rotation_list.append("UR")
            if self.checkRotation(i, j, "DR", rotation_matrix):
                rotation_list.append("DR")
        else:
            if self.checkRotation(i, j, "UDL", rotation_matrix):
                rotation_list.append("UDL")
            if self.checkRotation(i, j, "UDR", rotation_matrix):
                rotation_list.append("UDR")
            if self.checkRotation(i, j, "URL", rotation_matrix):
                rotation_list.append("URL")
            if self.checkRotation(i, j, "DRL", rotation_matrix):
                rotation_list.append("DRL")
        return rotation_list

    def solve(self):
        self.hash_node = {}
        return self.findState([["" for _ in range(self.n)] for _ in range(self.n)])

    def findState(self, rotation_matrix):
        score = 0
        options = []
        for i in range(self.n):
            for j in range(self.n):
                if rotation_matrix[i][j] == "":
                    rotation_list = self.findRotation(i, j, rotation_matrix)
                    if len(rotation_list) == 0:
                        return 0
                    else:
                        options = [((i, j), rotation) for rotation in rotation_list]
                        break
                else:
                    score += 1
            if options:
                break

        if score == self.target_score:
             return rotation_matrix

        self.visualizer.append(rotation_matrix)

        for op in options:
            copied_rotation_matrix = copy.deepcopy(rotation_matrix)
            (i, j), r = op
            copied_rotation_matrix[i][j] = r
            ans = self.findState(copied_rotation_matrix)
            if i == 0 and j == 0:
                i = 0
            if ans != 0:
                return ans
        return 0

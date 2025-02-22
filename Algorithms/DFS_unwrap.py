import copy

class DFS:
    def __init__(self, n, matrix):
        self.n = n
        self.target_score = n * n
        self.matrix = matrix

    def solve(self):
        return self.findState([["" for _ in range(self.n)] for _ in range(self.n)])

    def checkRotation(self, i, j, rotation, rotation_matrix):
        if 'U' in rotation:
            if i == 0 or not (rotation_matrix[i - 1][j] == "" or 'D' in rotation_matrix[i - 1][j]):
                return 0
        else:
            if i != 0 and 'D' in rotation_matrix[i - 1][j]:
                return 0

        if 'D' in rotation:
            if i == self.n - 1 or not (rotation_matrix[i + 1][j] == "" or 'U' in rotation_matrix[i + 1][j]):
                return 0
        else:
            if i != self.n - 1 and 'U' in rotation_matrix[i + 1][j]:
                return 0

        if 'L' in rotation:
            if j == 0 or not (rotation_matrix[i][j - 1] == "" or 'R' in rotation_matrix[i][j - 1]):
                return 0
        else:
            if j != 0 and 'R' in rotation_matrix[i][j - 1]:
                return 0

        if 'R' in rotation:
            if j == self.n - 1 or not (rotation_matrix[i][j + 1] == "" or 'L' in rotation_matrix[i][j + 1]):
                return 0
        else:
            if j != self.n - 1 and 'L' in rotation_matrix[i][j + 1]:
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

        for op in options:
            copied_rotation_matrix = copy.deepcopy(rotation_matrix)
            (i, j), r = op
            copied_rotation_matrix[i][j] = r
            ans = self.findState(copied_rotation_matrix)
            if ans != 0:
                return ans
        return 0

import copy

from Algorithms.DFS_wrap import DFS_wrap

class Greedy_wrap(DFS_wrap):
    def __init__(self, n, matrix):
        super().__init__(n, matrix)

    def solve(self):
        return self.findState([["" for _ in range(self.n)] for _ in range(self.n)])

    def isConnected(self, i, j, rotation_matrix):
        if i != 0:
            if 'D' in rotation_matrix[i - 1][j]:
                return 1
        elif 'D' in rotation_matrix[self.n - 1][j]:
            return 1
        if i != self.n - 1:
            if 'U' in rotation_matrix[i + 1][j]:
                return 1
        elif 'U' in rotation_matrix[0][j]:
            return 1

        if j != 0:
            if 'R' in rotation_matrix[i][j - 1]:
                return 1
        elif 'R' in rotation_matrix[i][self.n - 1]:
            return 1

        if j != self.n - 1:
            if 'L' in rotation_matrix[i][j + 1]:
                return 1
        elif 'L' in rotation_matrix[i][0]:
             return 1
        return 0

    def findState(self, rotation_matrix):
        repeat = 1
        while repeat == 1:
            repeat = 0
            options = []
            score = 0
            for i in range(self.n):
                for j in range(self.n):
                    if rotation_matrix[i][j] == "":
                        rotation_list = self.findRotation(i, j, rotation_matrix)
                        if len(rotation_list) == 1:
                            rotation_matrix[i][j] = rotation_list[0]
                            #self.ans(rotation_matrix)
                            repeat = 1
                            score += 1
                        if len(rotation_list) == 0:
                            return 0
                        if repeat == 0 and ((not options) or len(options) > len(rotation_list)):
                            if self.isConnected(i, j, rotation_matrix) == 1:
                                options = [((i, j), rotation) for rotation in rotation_list]
                    else:
                        score += 1

            if score == self.target_score:
                return self.deepChecker(rotation_matrix)
        
        if not options:
            for i in range(self.n):
                for j in range(self.n):
                    if rotation_matrix[i][j] == "":
                        rotation_list = self.findRotation(i, j, rotation_matrix)
                        if rotation_list:
                            options = [((i, j), rotation) for rotation in rotation_list]
                            break
                if options:
                    break

        for op in options:
            copied_rotation_matrix = copy.deepcopy(rotation_matrix)
            (i, j), r = op
            copied_rotation_matrix[i][j] = r
            ans = self.findState(copied_rotation_matrix)
            if ans != 0:
                return ans
        return 0

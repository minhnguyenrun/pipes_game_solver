import copy
from Algorithms.DFS_unwrap import DFS
from collections import deque

class Greedy(DFS):
    def __init__(self, n, matrix):
        super().__init__(n, matrix)
        self.visualizer = []

    def solve(self):
        self.rotation_matrix = [["" for _ in range(self.n)] for _ in range(self.n)]
        self.rotation_list_matrix = [[[] for _ in range(self.n)] for _ in range(self.n)]

        repeat = 1
        while repeat == 1:
            repeat = 0
            score = 0
            for i in range(self.n):
                for j in range(self.n):
                    if self.rotation_matrix[i][j] == "":
                        rotation_list = self.findRotation(i, j)
                        if len(rotation_list) == 1:
                            self.rotation_matrix[i][j] = rotation_list[0]
                            repeat = 1
                            score += 1
                        if len(rotation_list) == 0:
                            return 0
                        if repeat == 0:
                            self.rotation_list_matrix[i][j] = rotation_list
                    else:
                        score += 1

            if score == self.target_score:
                if self.deepChecker() != 0:
                    return self.rotation_matrix
                return 0

        next_i = None
        next_j = None
        for _i in range(self.n):
            for _j in range(self.n):
                if self.rotation_matrix[_i][_j] == "":
                    if next_i == None or len(self.rotation_list_matrix[_i][_j]) < len(self.rotation_list_matrix[next_i][next_j]):
                        next_i = _i
                        next_j = _j

        return self.findState(next_i, next_j)

    def isValid(self, pos):
        i, j = pos
        if i > -1 and j > -1 and i < self.n and j < self.n:
            return 1
        return 0

    def findState(self, i, j):
        my_rotation_list_matrix = copy.deepcopy(self.rotation_list_matrix[i][j])
        for rotation in my_rotation_list_matrix:
            self.rotation_matrix[i][j] = rotation
            queue = deque()
            auto_connected_cells = []
            old_rotation_list = {}
            UP = (i - 1, j)
            DOWN = (i + 1, j)
            LEFT = (i, j - 1)
            RIGHT = (i, j + 1)
            if self.isValid(UP): queue.append(UP)
            if self.isValid(DOWN): queue.append(DOWN)
            if self.isValid(LEFT): queue.append(LEFT)
            if self.isValid(RIGHT): queue.append(RIGHT)
            fail = 0

            while queue:
                _i, _j = queue.popleft()
                if self.rotation_matrix[_i][_j] != "":
                    continue
                rotation_list = self.findRotation(_i, _j)
                if len(rotation_list) == 0:
                    fail = 1
                    break
                elif len(rotation_list) == 1:
                    UP = (_i - 1, _j)
                    DOWN = (_i + 1, _j)
                    LEFT = (_i, _j - 1)
                    RIGHT = (_i, _j + 1)
                    if self.isValid(UP): queue.append(UP)
                    if self.isValid(DOWN): queue.append(DOWN)
                    if self.isValid(LEFT): queue.append(LEFT)
                    if self.isValid(RIGHT): queue.append(RIGHT)
                    auto_connected_cells.append((_i, _j))
                    self.rotation_matrix[_i][_j] = rotation_list[0]
                else:
                    if not (_i, _j) in old_rotation_list: old_rotation_list[(_i, _j)] = copy.deepcopy(self.rotation_list_matrix[_i][_j])
                    self.rotation_list_matrix[_i][_j] = rotation_list

            if fail == 0:
                self.visualizer.append(copy.deepcopy(self.rotation_matrix))
                next_i = None
                next_j = None
                for _i in range(self.n):
                    for _j in range(self.n):
                        if self.rotation_matrix[_i][_j] == "":
                            if next_i == None or len(self.rotation_list_matrix[_i][_j]) < len(self.rotation_list_matrix[next_i][next_j]):
                                next_i = _i
                                next_j = _j

                if next_i == None:
                    ans = self.deepChecker()
                    if ans != 0:
                        return ans
                    fail = 1

                if fail == 0:
                    ans = self.findState(next_i, next_j)
                    if ans != 0:
                        return ans

            for (_i, _j) in auto_connected_cells:
                self.rotation_matrix[_i][_j] = ""
            for (_i, _j) in old_rotation_list:
                self.rotation_list_matrix[_i][_j] = old_rotation_list[(_i, _j)]

        self.rotation_matrix[i][j] = ""
        self.rotation_list_matrix[i][j] = my_rotation_list_matrix
        return 0

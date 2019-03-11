# Ai assignment 2
# By Rohan Bhandari, Ujwal Narayan

# Input Format

# 4 4

# X/10 0 0 X
# 0 0 0 0
# 0 0 0 0
# 0 0 -X/5 0

# 3 2

# 0 0

# 0 3

# 3 2

# 0 1

# 2 2

# 3 0

# -X/10


import copy


class MDP:
    def __init__(self, board, start_state, end_states, walls, step_reward, discount):
        self.board = copy.deepcopy(board)
        self.start_state = start_state
        self.end_states = end_states
        self.walls = walls
        self.probabilities = [0.8, 0.1]
        self.step_reward = step_reward
        self.discount = discount
        self.delta = 0.01
        self.utility_map = [
            [0 for j in range(len(board[0]))] for i in range(len(board))]

    def value_iteration(self):
        cur_utility_map = copy.deepcopy(self.utility_map)
        while True:
            max_change = -1
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    new_utility = self.cal_utility(tuple(i, j))
                    val = (new_utility -
                           self.utility_map[i][j]) / self.utility_map[i][j]
                    max_change = max(max_change, val)
            if max_change <= self.delta:
                break
            self.utility_map = copy.deepcopy(cur_utility_map)

    def probability_cal(self, p1, p2, p3):
        return self.discount * (self.probabilities[0] * self.utility_map[p1[0]][p1[1]]
                                + self.probabilities[1] *
                                self.utility_map[p2[0]][p2[1]]
                                + self.probabilities[1] * self.utility_map[p3[0]][p3[1]])

    def cal_utility(self, coord):
        x, y = coord[0], coord[1]
        best_value = self.step_reward
        best_add = float('inf')
        # North, East, South, West
        next_state = {}
        next_state["north"] = next_state["east"] = next_state["south"] = next_state["west"] = (
            x, y)
        if x > 0:
            next_state["north"] = (x - 1, y)
        if y + 1 < len(self.board[x]):
            next_state["east"] = (x, y + 1)
        if x + 1 < len(self.board):
            next_state["south"] = (x + 1, y)
        if y > 0:
            next_state["west"] = (x, y - 1)

        val = self.probability_cal(
            next_state["north"], next_state["east"], next_state["west"])
        best_add = max(best_add, val)
        val = self.probability_cal(
            next_state["east"], next_state["north"], next_state["south"])
        best_add = max(best_add, val)
        val = self.probability_cal(
            next_state["south"], next_state["east"], next_state["west"])
        best_add = max(best_add, val)
        val = self.probability_cal(
            next_state["west"], next_state["north"], next_state["south"])
        best_add = max(best_add, val)
        best_value += best_add
        return best_value


def input():
    n, m = map(int, input().split())
    grid_world = []
    for i in range(n):
        grid_world.append([int(x) for x in input().split()])


# for i in range(n):
#     for j in range(m):
#         print(grid_world[i][j], end=' ')
#     print()

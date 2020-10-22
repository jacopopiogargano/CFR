from collections import defaultdict
from copy import copy
from typing import List, Tuple, Dict

from pkg.config import SIZE


class State:
    def __init__(self):
        self.winner = -99
        self.current_player = 0
        self.matrix = [[-99 for y in range(SIZE)] for x in range(SIZE)]
        self.history = tuple()

        self.regret = defaultdict(float)
        self.strategy = defaultdict(float)
        self.sigma = {0: defaultdict(lambda:
                                     defaultdict(lambda: 1 / len(self.get_legal_actions()) if len(
                                         self.get_legal_actions()) > 0 else 0)),
                      1: defaultdict(lambda:
                                     defaultdict(lambda: 1 / len(self.get_legal_actions()) if len(
                                         self.get_legal_actions()) > 0 else 0))}
        self.reach = defaultdict(lambda: 1)
        self.avg_strategy: Dict[List[Tuple], float] = {}

    def get_string_repr(self, show_strategy=False, strategy: Dict = None):
        _ = ""
        spaces = "     "
        for i in range(SIZE):
            for k in range(SIZE):
                if k % 2 == 0:
                    _ += (spaces + "|" + spaces + "|" + spaces)
                else:
                    for j in range(SIZE):
                        cell = self.matrix[i][j]
                        if show_strategy and cell < 0:
                            _ +=  str(int(round(strategy[(i, j)], 2)*100)).rjust(3) + '% '
                        else:
                            if cell < 0:
                                _ += spaces
                            else:
                                _ += '  ' + ('x' if not cell else 'o') + '  '
                        if j < SIZE - 1:
                            _ += '|'
                _ += '\n'
            if i < SIZE - 1:
                _ += '-----' + '|' + '-----' + '|' + '-----\n'
        return _

    def is_terminal(self):
        return len(self.get_legal_actions()) == 0 or self.winner >= 0

    # returns utility for player 0
    def get_utility(self):
        if self.is_terminal():
            if self.winner == 0:
                return 1
            elif self.winner == 1:
                return -1
            else:
                return 0
        else:
            raise Exception

    def get_legal_actions(self) -> List[Tuple]:
        legal_actions = []
        for i in range(SIZE):
            for j in range(SIZE):
                if self.is_legal_action(i, j):
                    legal_actions.append(tuple([i, j]))
        return legal_actions

    def is_legal_action(self, x, y):
        if x < 0 or x > SIZE or y < 0 or y > SIZE:
            return False
        return self.matrix[x][y] < 0

    # returns -99 if no winner, else winner
    def get_winner(self):
        def check_sum(s):
            if s == SIZE:
                return 1
            elif s == 0:
                return 0
            else:
                return -99

        for i in range(SIZE):
            s = sum(self.matrix[i])
            s = check_sum(s)
            if s >= 0:
                return s
        for j in range(SIZE):
            s = sum(self.matrix[i][j] for i in range(SIZE))
            s = check_sum(s)
            if s >= 0:
                return s

        if SIZE > 2:
            s = 0
            for i in range(SIZE):
                s += self.matrix[i][i]
            s = check_sum(s)
            if s >= 0:
                return s

            s = 0
            for i in range(SIZE - 1, -1, -1):
                s += self.matrix[i][SIZE - 1 - i]
            s = check_sum(s)
            if s >= 0:
                return s

        return -99

    def copy(self):
        new_state = State()
        new_state.winner = self.winner
        new_state.current_player = self.current_player
        new_state.matrix = [[y for y in x] for x in self.matrix]
        new_state.history = self.history
        return new_state

    def compute_avg_strategy(self):
        normalizing_sum = sum(self.strategy.values())
        actions = self.get_legal_actions()
        for a in actions:
            if normalizing_sum > 0:
                self.avg_strategy[a] = self.strategy[a] / normalizing_sum
            else:
                self.avg_strategy[a] = 1 / len(actions)

from collections import defaultdict

from pkg.env import TicTacToe
from pkg.state import State


class CFR:
    def __init__(self, env: TicTacToe):
        self.env = env
        self.max_regret = float('-inf')

    # i: the player (either 0 or 1)
    # p_0, p_1: the probabilities of the players reaching the state
    def cfr(self, s: State, i: int, p_0, p_1, t):
        if s.is_terminal():
            u = s.get_utility()
            return u if i == 0 else -u
        else:
            v = 0
            actions = s.get_legal_actions()
            v_a = defaultdict(float)
            for a in actions:
                s_child = self.env.get_state(s, a[0], a[1])
                if s.current_player == 0:
                    s_child.reach[t] = s.reach[t] * s.sigma[0][t][a]
                    v_a[a] = self.cfr(s_child, i, p_0 * s.sigma[0][t][a], p_1, t)
                else:
                    s_child.reach[t] = s.reach[t] * s.sigma[1][t][a]
                    v_a[a] = self.cfr(s_child, i, p_0, p_1 * s.sigma[1][t][a], t)
                v += s.sigma[i][t][a] * v_a[a]

            p_player = p_0 if i == 0 else p_1
            p_opponent = p_1 if i == 0 else p_0

            if s.current_player == i:
                for a in actions:
                    s.regret[a] += p_opponent * (v_a[a] - v)
                    s.strategy[a] += p_player * s.sigma[i][t][a]
                    self.max_regret = max(self.max_regret, s.regret[a])

                # regret matching
                regret_sum = sum([max(x, 0) for x in s.regret.values()])
                for a in actions:
                    if regret_sum > 0:
                        s.sigma[i][t + 1][a] = max(s.regret[a], 0) / regret_sum
                    else:
                        s.sigma[i][t + 1][a] = 1 / len(actions)
            return v

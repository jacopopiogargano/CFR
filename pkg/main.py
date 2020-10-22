from pkg.cfr import CFR
from pkg.config import *
from pkg.env import TicTacToe
from pkg.utils import *

print("Setting up environment..this may take a while")
env = TicTacToe(generate_states=GEN_STATES)
print("Done!")
s_0 = env.states[()]

cfr = CFR(env)
for t in range(T):
    print("ITERATION: ", t)
    for i in range(2):
        cfr.cfr(s_0, i, 1, 1, t)
    env.regrets.append(cfr.max_regret / (t + 1))
    for s in env.states.values():
        try:
            del s.sigma[0][t]
            del s.sigma[1][t]
        except:
            pass
    if GEN_STATES and t == 0:
        save_states(env.states)

compute_and_save_strategy(list(env.states.values()))
plot_regrets(env.regrets)

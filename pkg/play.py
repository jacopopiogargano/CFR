import numpy as np

from pkg.config import SIZE
from pkg.env import TicTacToe
from pkg.state import State
from pkg.utils import get_history_to_strategy

print("Generating Env")
env = TicTacToe(generate_states=True)
print("Fetching history to strategy..this may take a while")
history_to_strategy = get_history_to_strategy()
print("Fetched!")

while True:
    print("\n\nWELCOME!!\n\n")
    print("Do you want to be player 1? [y/n]")
    a = input()
    AI_player = 1 if a == 'y' else 0

    s = State()
    while not s.is_terminal():
        print("current player: ", s.current_player)

        if s.current_player == AI_player:
            strategy = history_to_strategy[s.history]
            print(s.get_string_repr(show_strategy=True, strategy=strategy))
            action_index = np.random.choice([x for x in range(len(strategy.keys()))], p=list(strategy.values()))
            action = list(strategy.keys())[action_index]
            x, y = action[0], action[1]
        else:
            x, y = -1, -1
            while x < 0 or x >= SIZE or y < 0 or y >= SIZE:
                print(s.get_string_repr())
                print("Choose x: ", end="")
                x = int(input())
                print("Choose y: ", end="")
                y = int(input())

        s = env.get_state(s, x, y)

    print(s.get_string_repr())
    if s.winner < 0:
        print("TIE!!")
    else:
        print("WINNER: ", s.winner)

    print("\n\n\nPress any key for a new game!")
    input()

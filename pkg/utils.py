from typing import Tuple, Dict, List
import jsonpickle as jp
import matplotlib.pyplot as plt

from pkg.config import SIZE
from pkg.state import State


def get_states() -> Dict[Tuple, State]:
    with open('resources/' + str(SIZE) + '/states.txt', 'r') as json_file:
        return jp.decode(json_file.read(), keys=True)


def save_states(states: Dict[Tuple, State]):
    with open('resources/' + str(SIZE) + '/states.txt', 'w') as json_file:
        json_file.write(jp.encode(states, keys=True))


def plot_regrets(regrets: List[float]):
    plt.plot([t for t in range(len(regrets))], regrets)
    plt.show()


def compute_and_save_strategy(states: List[State]):
    history_to_strategy = {}
    for s in states:
        print(s.history)
        s.compute_avg_strategy()
        history_to_strategy[s.history] = s.avg_strategy
    with open('output/' + str(SIZE) + '/strategy.txt', 'w') as json_file:
        json_file.write(jp.encode(history_to_strategy, keys=True))


def get_history_to_strategy() -> Dict[Tuple[Tuple], Dict[Tuple, float]]:
    with open('output/' + str(SIZE) + '/strategy.txt', 'r') as json_file:
        return jp.decode(json_file.read(), keys=True)

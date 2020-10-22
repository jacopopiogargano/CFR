from typing import Dict, Tuple

from pkg.config import SIZE
from pkg.state import State
from pkg.utils import get_states


class TicTacToe:
    def __init__(self, generate_states=False):
        if not generate_states:
            self.states: Dict[Tuple, State] = get_states()
        else:
            self.states: Dict[Tuple, State] = {(): State()}
        self.regrets = []

    def _next_state(self, state: State, x, y) -> State:
        new_state: State = state.copy()
        if new_state.is_legal_action(x, y):
            new_state.matrix[x][y] = state.current_player
            new_state.current_player = 1 - new_state.current_player
            new_state.winner = new_state.get_winner()
            new_state.history = self.new_history(state, x, y)
            self.states[new_state.history] = new_state
        return new_state

    def get_state(self, state, x, y) -> State:
        history = self.new_history(state, x, y)
        s = self.states.get(history, None)
        if s is None:
            s = self._next_state(state, x, y)
        return s

    def new_history(self, state, x, y):
        return tuple((list(state.history)) + [tuple([x, y])])

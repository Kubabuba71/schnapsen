#!/usr/bin/env python
"""


"""

import random

from api import State, util


class Bot:

    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=8):
        """
        :param randomize: Whether to select randomly from moves of equal value (or to select the first always)
        :param depth:
        """
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        player = state.whose_turn()

        val, move = self.value(state, player=player)

        return move

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0, player = -1):
        """
        Return the value of this state and the associated move
        :param State state:
        :param float alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param float beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param int depth: How deep we are in the tree
        :return val, move: the value of the state, and the best move.
        """

        if state.finished():
            winner, points = state.winner()
            return (points, None) if winner == 1 else (-points, None)

        if depth == self.__max_depth:
            return heuristic(state, player)

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            value, _ = self.value(state.next(move), alpha, beta, depth+1, player)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            # Prune the search tree
            # We know this state will never be chosen, so we stop evaluating its children
            if beta < alpha:
                break

        return best_value, best_move

def maximizing(state):
    # type: (State) -> bool
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1

# def heuristic(state):
#     return state.get_points(state.whose_turn()) / 66, None

# def heuristic(state):
#     """
#     Original Heuristic
#     """
#     return util.ratio_points(state, 1) * 2.0 - 1.0, None

def heuristic(state, player):
    return state.get_points(player) / 66, None
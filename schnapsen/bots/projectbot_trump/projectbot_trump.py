#!/usr/bin/env python
"""
This is a bot that applies propositional logic reasoning to determine its strategy.
The strategy it uses is determined by what is defined in load.py. Here it is to always
pick a Jack to play whenever this is a legal move.

It loads general information about the game, as well as the definition of a strategy,
from load.py.
"""

import random

import load
from api import Deck, State
from kb import KB, Boolean, Integer


class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        # moves = state.moves()
        moves = sorted(state.moves(), key=lambda tup: tup[0], reverse=True)

        random.shuffle(moves)

        for move in moves:

            if not self.kb_consistent_trumpmarriage(state, move):
                # Plays the first move that makes the kb inconsistent. We do not take
                # into account that there might be other valid moves according to the strategy.
                # Uncomment the next line if you want to see that something happens.
                print "Trump Marriage"
                return move

        for move in moves:

            if not self.kb_trump(state, move):
                # Plays the first move that makes the kb inconsistent. We do not take
                # into account that there might be other valid moves according to the strategy.
                # Uncomment the next line if you want to see that something happens.
                print "Strategy Applied"
                return move

        # If no move that is entailed by the kb is found, play random move
        return random.choice(moves)


    # Note: In this example, the state object is not used,
    # but you might want to do it for your own strategy.
    def kb_trump(self,state,move):

        # type: (State,move) -> bool

        kb = KB()

        load.general_information(kb)
        load.strategy_knowledge(kb)

        p_card = move[0]
        p_card_suit = Deck.get_suit(p_card)

        trump_suit = state.get_trump_suit()

        variable_string = "wtt" + str(p_card_suit) + str(trump_suit)
        strategy_variable = Boolean(variable_string)


        kb.add_clause(~strategy_variable)

        return kb.satisfiable()

    def kb_consistent_trumpmarriage(self, state, move):
        # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)

        if suit == "C":
            card1 = 2
            card2 = 3
            variable_string = "m" + str(card1) + str(card2)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "D":
            card1 = 7
            card2 = 8
            variable_string = "m" + str(card1) + str(card2)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "H":
            card1 = 12
            card2 = 13
            variable_string = "m" + str(card1) + str(card2)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "S":
            card1 = 17
            card2 = 18
            variable_string = "m" + str(card1) + str(card2)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)

        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "pm" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

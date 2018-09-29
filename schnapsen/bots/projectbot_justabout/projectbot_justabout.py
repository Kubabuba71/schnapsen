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

        player = state.whose_turn()
        on_lead = state.leader()

        if player == on_lead:

            # If no move that is entailed by the kb is found, play random move
            print "random move made - on lead"
            return random.choice(moves)
        else:

            #Lowest matching trick winning card
            for move in moves:
                if not self.kb_consistent_matching_win(state,move):
                    print "Matching suit card win strategy applied"
                    return move

            for move in moves:
                if not self.kb_consistent_trump_win(state,move):
                    print "Trump card win strategy applied"
                    return move

            # If no move that is entailed by the kb is found, play random move
            print "random move made - not on lead"
            return random.choice(moves)

    # Note: In this example, the state object is not used,
    # but you might want to do it for your own strategy.
    def kb_consistent_low_non_trump(self, state, move):
        # type: (State, move) -> bool

        kb = KB()

        load.general_information(kb)
        load.strategy_knowledge(kb)

        card = move[0]
        trump_suit = state.get_trump_suit()

        variable_string = "pc" + str(card) + str(trump_suit)
        strategy_variable = Boolean(variable_string)

        kb.add_clause(~strategy_variable)

        return kb.satisfiable()


    def kb_consistent_matching_win(self, state, move):

        # type: (State,move) -> bool

        kb = KB()
        load.general_information(kb)
        load.strategy_knowledge(kb)

        opp_card = state.get_opponents_played_card()
        opp_card_suit = Deck.get_suit(opp_card)
        opp_card_rank = opp_card % 5

        p_card = move[0]
        p_card_suit = Deck.get_suit(p_card)
        p_card_rank = opp_card % 5

        variable_string = "wt" + str(p_card_rank) + str(opp_card_rank) + str(p_card_suit) + str(opp_card_suit)
        strategy_variable = Boolean(variable_string)

        kb.add_clause(~strategy_variable)

        return kb.satisfiable()

    def kb_consistent_trump_win(self,state,move):

        # type: (State,move) -> bool

        kb = KB()

        load.general_information(kb)
        load.strategy_knowledge(kb)

        opp_card = state.get_opponents_played_card()
        opp_card_suit = Deck.get_suit(opp_card)
        opp_card_rank = opp_card & 5

        p_card = move[0]
        p_card_suit = Deck.get_suit(p_card)
        p_card_rank = p_card % 5

        trump_suit = state.get_trump_suit()

        constraint_a = Integer('me') > Integer('op')
        constraint_b = Integer('op') > Integer('me')

        if opp_card_suit == trump_suit:
            if p_card_suit == trump_suit:
                if opp_card_rank < p_card_rank:
                    strategy_variable = constraint_b
                else:
                    strategy_variable = constraint_a
            else:
                strategy_variable = constraint_b
        else:
            variable_string = "wtt" + str(p_card_suit) + str(trump_suit)
            strategy_variable = Boolean(variable_string)


        kb.add_clause(~strategy_variable)

        return kb.satisfiable()

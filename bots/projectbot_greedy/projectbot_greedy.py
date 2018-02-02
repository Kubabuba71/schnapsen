#!/usr/bin/env python
"""
This is a bot that applies propositional logic reasoning to determine its strategy.
The strategy it uses is determined by what is defined in load.py. Here it is to always
pick a Jack to play whenever this is a legal move.

It loads general information about the game, as well as the definition of a strategy,
from load.py.
"""

from api import State, Deck
import random, load

from kb import KB, Boolean, Integer

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):

        # moves = state.moves()
        moves = sorted(state.moves(), key=lambda tup: tup[0], reverse=True)

        random.shuffle(moves)

        # Check for possible weddings
        for move in moves:

            if not self.kb_consistent_marriage(state, move):
                # print "Wedding strategy applied"
                return move

        for move in moves:

            if not self.kb_consistent_trumpace(state, move):
                # print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpten(state, move):
                # print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpking(state, move):
                # print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpqueen(state, move):
                # print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpjack(state, move):
                # print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_ace(state, move):
                # print "Played ACE"
                return move

        for move in moves:

            if not self.kb_ten(state, move):
                # print "Played Ten"
                return move

        for move in moves:

            if not self.kb_king(state, move):
                # print "Played King"
                return move

        for move in moves:

            if not self.kb_queen(state, move):
                # print "Played Queen"
                return move

        for move in moves:

            if not self.kb_jack(state, move):
                # print "Played Jack"
                return move

            # If no move that is entailed by the kb is found, play random move
        return random.choice(moves)

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

    def kb_ace(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load.general_information(kb)


        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pa" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()

    def kb_ten(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load.general_information(kb)


        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pt" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()

    def kb_king(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load.general_information(kb)


        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pk" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()

    def kb_queen(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load.general_information(kb)


        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pq" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()

    def kb_jack(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        # This creates the string which is used to make the strategy_variable.
        # Note that as far as kb.py is concerned, two objects created with the same
        # string in the constructor are equivalent, and are seen as the same symbol.
        # Here we use "pj" to indicate that the card with index "index" should be played with the
        # PlayJack heuristics that was defined in class. Initialise a different variable if
        # you want to apply a different strategy (that you will have to define in load.py)
        variable_string = "pj" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)
        return kb.satisfiable()

    def kb_consistent_trumpace(self, state, move):
        # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)

        if suit == "C":
            index = 0
            variable_string = "ta" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "D":
            index = 5
            variable_string = "ta" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "H":
            index = 10
            variable_string = "ta" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "S":
            index = 15
            variable_string = "ta" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)

        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "pta" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

    def kb_consistent_trumpten(self, state, move):
        # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)

        if suit == "C":
            index = 1
            variable_string = "tt" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "D":
            index = 6
            variable_string = "tt" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "H":
            index = 11
            variable_string = "tt" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "S":
            index = 16
            variable_string = "tt" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)

        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "ptt" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

    def kb_consistent_trumpking(self, state, move):
        # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)

        if suit == "C":
            index = 2
            variable_string = "tk" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "D":
            index = 7
            variable_string = "tk" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "H":
            index = 12
            variable_string = "tk" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "S":
            index = 17
            variable_string = "tk" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)

        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "ptk" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

    def kb_consistent_trumpqueen(self, state, move):
        # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)

        if suit == "C":
            index = 3
            variable_string = "tq" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "D":
            index = 8
            variable_string = "tq" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "H":
            index = 13
            variable_string = "tq" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "S":
            index = 18
            variable_string = "tq" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)

        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "ptq" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

    def kb_consistent_trumpjack(self, state, move):
        # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game

        suit = State.get_trump_suit(state)

        if suit == "C":
            index = 4
            variable_string = "tj" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "D":
            index = 9
            variable_string = "tj" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "H":
            index = 14
            variable_string = "tj" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)
        elif suit == "S":
            index = 19
            variable_string = "tj" + str(index)
            strategy_variable = Boolean(variable_string)
            kb.add_clause(strategy_variable)

        load.general_information(kb)

        # Add the necessary knowledge about the strategy
        load.strategy_knowledge(kb)

        # This line stores the index of the card in the deck.
        # If this doesn't make sense, refer to _deck.py for the card index mapping
        index = move[0]

        variable_string = "ptj" + str(index)
        strategy_variable = Boolean(variable_string)

        # Add the relevant clause to the loaded knowledge base
        kb.add_clause(~strategy_variable)

        # If the knowledge base is not satisfiable, the strategy variable is
        # entailed (proof by refutation)

        return kb.satisfiable()

    def kb_consistent_marriage(self, state, move):
        # type: (State, move) -> bool

        kb = KB()
        load.general_information(kb)
        load.strategy_knowledge(kb)

        card1 = move[0]
        card2 = move[1]

        variable_string = "m" + str(card1) + str(card2)

        strategy_variable = Boolean(variable_string)
        kb.add_clause(~strategy_variable)
        return kb.satisfiable()









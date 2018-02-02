"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State, util, Deck
import random
from kb import KB, Boolean, Integer
import load_ace, load_conservative, load_greedy, load_justabout, load_trump

going_first_amount = 0
winning_game_amount = 0

no_trump_amount = 0
no_ace_amount = 0
at_least_2_trump = 0
at_least_1_marriage = 0
cant_win_trick_amount = 0


class Bot:
    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.
        Be sure to make a legal move. Illegal moves, like giving an index of a card you
        don't own or proposing an illegal mariage, will lose you the game.
       	TODO: add some more explanation
        :param State state: An object representing the gamestate. This includes a link to
            the states of all the cards, the trick and the points.
        :return: A tuple of integers or a tuple of an integer and None,
            indicating a move; the first indicates the card played in the trick, the second a
            potential spouse.
        """

        if self.going_first(state) and self.no_trump_cards(state):
            # move = self.play_conservative(state)
            # move = self.play_greedy(state)
            # move = self.play_trump_card(state)
            # move = self.play_ace_card(state)
            move = self.play_card_to_win_trick(state)
        else:
            move = random.choice(state.moves())

        return move

    def get_suit_of_move(self, move):
        if move[0] < 5:
                suit = 'C'
        elif move[0] < 10:
            suit = 'D'
        elif move[0] < 15:
            suit = 'H'
        elif move[0] < 20:
            suit = 'S'
        return suit

    def is_king(self, move):
        if move[0] == 2 or move[0] == 7 or move[0] == 12 or move[0] == 17: return True
        return False

    def is_queen(self, move):
        if move[0] == 3 or move[0] == 8 or move[0] == 13 or move[0] == 18: return True
        return False

    def no_trump_cards(self, state):
        trump_suit = state.get_trump_suit()
        for move in state.moves():
            suit = self.get_suit_of_move(move)
            if suit == trump_suit:
                return False

        return True

    def no_ace_cards(self, state):
        for move in state.moves():
            if move[0] is not None and move[0] % 5 == 0:
                return False
        return True

    def at_least_two_trump_cards(self, state):
        num_of_trump_cards = 0
        trump_suit = state.get_trump_suit()
        for move in state.moves():
            if self.get_suit_of_move(move) == trump_suit:
                num_of_trump_cards += 1
        if num_of_trump_cards >= 2: return True
        return False

    def at_least_one_marriage(self, state):
        moves = state.moves()
        leader = state.leader()
        current_player = state.whose_turn()
        
        if(leader == current_player):
            for move in moves:
                if self.is_king(move):
                    king_suit = self.get_suit_of_move(move)
                    for move in moves:
                        queen_suit = self.get_suit_of_move(move)
                        if self.is_queen(move) and king_suit == queen_suit:
                            return True
        return False

    def cant_win_trick(self, state):
        player = state.whose_turn()
        opponent = util.other(player)
        leader = state.leader()
        if opponent == leader:
            opponents_played_card = state.get_opponents_played_card()
            current_opponent_points = state.get_points(opponent)

            current_points = state.get_points(player)
            for move in state.moves():
                next_state = state.next(move)
                future_opponent_points = next_state.get_points(opponent)

                future_points = next_state.get_points(player)

                points_gained = future_points - future_opponent_points
                if(points_gained <= 0): return True
        return False

    def going_first(self, state):
        player = state.whose_turn()
        leader = state.leader()
        return player == leader

    def winning_game(self, state):
        player = state. whose_turn()
        opponent = util.other(player)

        player_points = state.get_points(player)
        opponent_points = state.get_points(opponent)

        return opponent_points < player_points

    def play_conservative(self, state):
        moves = sorted(state.moves(), key=lambda tup: tup[0], reverse=True)

        random.shuffle(moves)


        # Low non trump moves
        for move in moves:
            if not self.kb_consistent_low_non_trump(state, move):
                print "Low non trump strategy applied"
                return move

        # If no move that is entailed by the kb is found, play random move
        print "random move made - on lead"
        return random.choice(moves)

    def kb_consistent_matching_win(self, state, move):

        # type: (State,move) -> bool

        kb = KB()
        load_conservative.general_information(kb)
        load_conservative.strategy_knowledge(kb)

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

    def play_greedy(self, state):
        moves = sorted(state.moves(), key=lambda tup: tup[0], reverse=True)

        random.shuffle(moves)

        # Check for possible weddings
        for move in moves:

            if not self.kb_consistent_marriage(state, move):
                print "Wedding strategy applied"
                return move

        for move in moves:

            if not self.kb_consistent_trumpace(state, move):
                print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpten(state, move):
                print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpking(state, move):
                print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpqueen(state, move):
                print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_consistent_trumpjack(state, move):
                print "Played Trump Ace"
                return move

        for move in moves:

            if not self.kb_ace(state, move):
                print "Played ACE"
                return move

        for move in moves:

            if not self.kb_ten(state, move):
                print "Played Ten"
                return move

        for move in moves:

            if not self.kb_king(state, move):
                print "Played King"
                return move

        for move in moves:

            if not self.kb_queen(state, move):
                print "Played Queen"
                return move

        for move in moves:

            if not self.kb_jack(state, move):
                print "Played Jack"
                return move

            # If no move that is entailed by the kb is found, play random move
        return random.choice(moves)

    def kb_trump(self,state,move):

        # type: (State,move) -> bool

        kb = KB()

        load_greedy.general_information(kb)
        load_greedy.strategy_knowledge(kb)

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
        load_greedy.general_information(kb)


        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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
        load_greedy.general_information(kb)


        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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
        load_greedy.general_information(kb)


        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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
        load_greedy.general_information(kb)


        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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
        load_greedy.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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

        load_greedy.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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

        load_greedy.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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

        load_greedy.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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

        load_greedy.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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

        load_greedy.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_greedy.strategy_knowledge(kb)

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
        load_greedy.general_information(kb)
        load_greedy.strategy_knowledge(kb)

        card1 = move[0]
        card2 = move[1]

        variable_string = "m" + str(card1) + str(card2)

        strategy_variable = Boolean(variable_string)
        kb.add_clause(~strategy_variable)
        return kb.satisfiable()

    def play_trump_card(self, state):
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

    def kb_trump(self,state,move):

        # type: (State,move) -> bool

        kb = KB()

        load_trump.general_information(kb)
        load_trump.strategy_knowledge(kb)

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

        load_trump.general_information(kb)

        # Add the necessary knowledge about the strategy
        load_trump.strategy_knowledge(kb)

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

    def play_ace_card(self, state):
        # moves = state.moves()
        moves = sorted(state.moves(), key=lambda tup: tup[0], reverse=True)

        random.shuffle(moves)

        for move in moves:

            if not self.kb_consistent(state, move):
                # Plays the first move that makes the kb inconsistent. We do not take
                # into account that there might be other valid moves according to the strategy.
                # Uncomment the next line if you want to see that something happens.
                print "Strategy Applied"
                return move

        # If no move that is entailed by the kb is found, play random move
        return random.choice(moves)

    def kb_consistent(self, state, move):
    # type: (State, move) -> bool

        # each time we check for consistency we initialise a new knowledge-base
        kb = KB()

        # Add general information about the game
        load_ace.general_information(kb)


        # Add the necessary knowledge about the strategy
        load_ace.strategy_knowledge(kb)

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

    def play_random(self, state):
        moves = state.moves()


        # Return a random choice
        return random.choice(moves)

    def play_card_to_win_trick(self, state):
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

    def kb_consistent_low_non_trump(self, state, move):
        # type: (State, move) -> bool

        kb = KB()

        load_justabout.general_information(kb)
        load_justabout.strategy_knowledge(kb)

        card = move[0]
        trump_suit = state.get_trump_suit()

        variable_string = "pc" + str(card) + str(trump_suit)
        strategy_variable = Boolean(variable_string)

        kb.add_clause(~strategy_variable)

        return kb.satisfiable()

    def kb_consistent_matching_win(self, state, move):

        # type: (State,move) -> bool

        kb = KB()
        load_justabout.general_information(kb)
        load_justabout.strategy_knowledge(kb)

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

        load_justabout.general_information(kb)
        load_justabout.strategy_knowledge(kb)

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
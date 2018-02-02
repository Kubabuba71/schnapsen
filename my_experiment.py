from api import State, Deck, engine
from api import util
import numpy
import random

STATE_RUNS = 100000

def going_first(state):
    leader = state.leader()
    return 1 == leader

if __name__ == "__main__":
    REPEATS = 100
    PHASE = 2
    going_first_num = 0
    going_second_num = 0


    bot1 = "projectbot"
    bot2 = "rand"
    bots = []
    bots.append(util.load_player(bot1))#player1
    bots.append(util.load_player(bot2))#player2

    print("Bot1: ", bot1)
    print("Bot2: ", bot2)

    n = len(bots)
    wins = [0] * len(bots)
    matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

    totalgames = (n*n - n)/2 * REPEATS
    playedgames = 0

    print('Playing {} games:'.format(totalgames))

    r = 0
    played_games = 0

    print(matches)
    while played_games < totalgames:
    # for r in range(REPEATS):
        for a, b in matches:
            print("Playing game: " , r)

            # Generate a state with a random seed
            start = State.generate(r, phase=int(PHASE))
            r += 1

            if not going_first(start):
                print("Leader was ", start.whose_turn(), " continuing")
                continue
            else:
                if random.choice([True, False]):
                    p = [a, b]
                else:
                    p = [b, a]
                # going_second_num += 1
                going_first_num += 1
                print("leader: ", start.whose_turn())
                winner = engine.play(bots[0], bots[1], start, verbose=False)
                played_games += 1

                #TODO: ALSO IMPLEMENT POINTS FOR WINNING
                if winner is not None:
                    winner = p[winner[0] - 1]
                    wins[winner] += 1

                playedgames += 1
                print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

    print("first", going_first_num)
    print("second", going_second_num)
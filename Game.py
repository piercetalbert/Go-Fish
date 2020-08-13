from collections import defaultdict
from collections import OrderedDict
import random
import time
from Card import Card
from Deck import Deck
from Turn import Turn
from Player import Player
from AIPlayer import AIPlayer
import Constants


class Game:

    def __init__(self):
        # self.card = Card()
        self.deck = Deck()
        self.turn = Turn()

        self.hands = defaultdict(list)
        self.scores = OrderedDict()
        self.players = []
        self.draw_pile = []
        self.player_books = 0
        self.ai_books = 0

        self.human_pl = self.get_human_player()

        self.generate_ai_players()
        self.deal_cards()
        self.take_turns()
        self.victory_conditions()

    def get_human_player(self):
        # first, let's instantiate our human player and add them to our list of players
        print("")
        username = input("Enter name: ")
        player = Player(username, self.player_books)
        self.players.append(player)

        return player.name

    def generate_ai_players(self):

        while True:
            print("")
            num_ai_players = input("Enter number of AI: ")
            num_ai_players = int(num_ai_players)

            # max 4 AI players
            if num_ai_players > 4:
                print("")
                print("Too many players.")
                continue
            elif num_ai_players < 1:
                print("")
                print("Not enough players.")
            else:
                break

        # select AI name at random
        def generate_name(ai_names):
            name = random.choice(ai_names)
            ai_names.remove(name)
            return name

        # add the AI to our players
        for x in range(num_ai_players):
            ai_name = generate_name(Constants.AI_NAMES)
            ai_player = AIPlayer(ai_name, self.ai_books)
            self.players.append(ai_player)

    def deal_cards(self):
        # build and shuffle our deck before we deal
        play_Deck = self.deck.build_deck()
        play_Deck = self.deck.shuffle_deck(play_Deck)
        num_players = len(self.players)

        if num_players == 4 or num_players == 5:
            cards_each = Constants.CARDS_EACH_5
        elif num_players == 2 or num_players == 3:
            cards_each = Constants.CARDS_EACH_7
        else:
            print("ERROR: total number of players not aligned with number of AI players.")
            quit()

        # deal hands
        for x in range(num_players):
            self.hands[self.players[x].name] = self.deck.deal_hand(play_Deck, cards_each)

        # we use the remaining deck as the draw pile
        # and sort the hands
        self.draw_pile = play_Deck

    def play_order(self, players):
        # player order is random
        player_order = players
        random.shuffle(player_order)
        return player_order

    def next_player(self, player, player_order, num_players):
        # get current position with the index of the current player
        current_position = player_order.index(player)

        # if the current position is not the last player in the list, iterate 1
        # otherwise reset to the beginning position
        if current_position < (num_players - 1):
            next = player_order[current_position + 1]
            current_position += 1
        else:
            next = player_order[0]
        return next

    def take_turns(self):
        tmp = self.play_order(self.players)
        ord = []
        x = 0

        # we make a new list with just names and order of the  players
        while x < len(tmp):
            ord.append(tmp[x].name)
            x += 1

        num_players = len(ord)
        nxt = ord[0]
        human_index = ord.index(self.human_pl)

        while True:
            print("\n")
            # check if if the next player is human or AI, call its turn function
            if nxt == ord[human_index]:
                print("-------------------------")
                print(ord[human_index] + "'s turn." + " | ", tmp[human_index].books, "BOOKS")
                tmp[human_index].play_turn(self.hands, self.draw_pile, ord[human_index])
                print("-------------------------")
                time.sleep(1)
            else:
                ai_index = ord.index(nxt)
                print("-------------------------")
                print(nxt + "'s turn." + " | ", tmp[ai_index].books, "BOOKS")
                tmp[ai_index].ai_turn(self.hands, self.draw_pile, nxt, self.players)
                print("-------------------------")
                time.sleep(1)
            nxt = self.next_player(nxt, ord, num_players)

            # if all hands are empty, stop playing turns
            if all(not y for y in self.hands.values()):
                break
            else:
                continue

    def victory_conditions(self):
        for x in self.players:
            self.scores[x.name] = x.books

        # sort scores by value with lambda expression
        sorted_scores = OrderedDict(sorted(self.scores.items(),
                                           key=lambda kv: kv[1], reverse=True))

        # get winning score from max() of scores
        score_vals = list(self.scores.values())
        winning_score = max(score_vals)

        # if there are more than one max value, ends in tie
        if score_vals.count(winning_score) > 1:
            print("")
            print("**********")
            print("GAME OVER")
            print("**********")
            print("")
            print("TIE")
            print("")
            print("SCORES: ")
            for x in sorted_scores:
                print(x, ":", sorted_scores[x])
            print("")

        # otherwise declare a winner
        else:
            for name, score in self.scores.items():
                winner = max(self.scores, key=self.scores.get)

            print("")
            print("**********")
            print("GAME OVER")
            print("**********")
            print("")
            print("* WINNER: " + winner + " *")
            print("")
            print("SCORES: ")
            print("----------")
            for x in sorted_scores:
                print(x, ":", sorted_scores[x])
            print("")

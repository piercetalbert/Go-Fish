import random
import time
from collections import defaultdict
from Turn import Turn
from Card import Card
from Player import Player


class AIPlayer(Player):

    def __init__(self, name, books):
        super(AIPlayer, self).__init__(name, books)

        self.previous_player = None
        self.previous_card = None

    def ai_turn(self, hands, draw_pile, player, players):

        print("")
        self.turn.see_current_hand(hands, player)

        previous_moves = []

        cards_taken = 1
        while cards_taken > 0:
            cards_taken = 0
            ai_hand = list(hands[player])

            if len(ai_hand) > 0:

                table = []

                ##table contains the eligible players to ask
                # removes itself and any players who have 0 cards
                for x in players:
                    if x.name == player:
                        continue
                    elif not hands[x.name]:
                        continue
                    else:
                        table.append(x)

                # default move
                pl = self.__ai_choose_player(table, hands, player, players)
                crd = self.__ai_choose_card(ai_hand, player, pl, players)
                move = (pl, crd)

                # check if this is the AIs first turn, if yes do not evaluate previous cards
                if self.previous_player == None or self.previous_card == None:
                    pl = self.__ai_choose_player(table, hands, player, players)
                    crd = self.__ai_choose_card(ai_hand, player, pl, players)

                ##if the move is equal to any previous move this turn,
                # choose a different player to ask
                else:
                    if move in previous_moves:
                        table.remove(pl)
                        pl = self.__ai_choose_player(table, hands, player, players)
                        crd = self.__ai_choose_card(ai_hand, player, pl, players)

                self.cards_asked.append(crd)
                self.previous_player = pl
                self.previous_card = crd
                previous_move = (self.previous_player, self.previous_card)
                previous_moves.append(previous_move)

                # ask for cards as long as its hand has cards
                time.sleep(0.2)
                print("")
                print(pl.name + ", do you have any " + crd.rank + "'s?")
                cards_taken = self.turn.ask_for_card(hands, crd, player, pl.name)
                self.books = self.create_book(hands, player, self.books)
            else:
                print("")
                print("Hand empty!")
                break

        ##check if the draw pile has cards, and draw
        # also do another check if a book can be made
        if len(draw_pile) > 0:
            turn = Turn()
            fished_card = turn.go_fish(draw_pile, hands, player)
            self.books = self.create_book(hands, player, self.books)
            time.sleep(0.2)
            print("")
            print("Go fish!")
        else:
            print("")
            print("Draw pile empty!")

    def __ai_choose_card(self, ai_hand, player, ask_player, players):
        # check if the target player has asked for a card currently in the AIs hand,
        # then pick that card to ask the target player
        for x in ai_hand:
            for y in ask_player.cards_asked:
                if x.rank == y.rank:
                    ask_card = x
                    return ask_card

        # otherwise, pick it at random from its hand
        ask_card = random.choice(ai_hand)

        return ask_card

    def __ai_choose_player(self, table, hands, player, players):
        # pick a random player
        ask_player = random.choice(table)

        return ask_player

import random
from collections import defaultdict
from Card import Card
import Constants


class Deck:

    def __init__(self):
        self.DECK = []

    # Create full deck
    def build_deck(self):

        x = 0
        y = 0
        z = 0

        while x < 4:
            while y < 13:
                card = Card(Constants.RANK[y], Constants.SUIT[x])
                self.DECK.append(card)
                y += 1
                z += 1
            x += 1
            y = 0

        return self.DECK

    # take the rop card off the deck
    def deal_top_card(self, deck):
        top_card = deck[0]
        deck.pop(0)
        return top_card

    # take a random card from the deck
    def get_random_card(self, deck):
        random_card = random.choice(deck)
        return random_card

    # shuffle the deck
    def shuffle_deck(self, deck):
        random.shuffle(deck)
        return deck

    # deal hand to players based on specified hand size
    def deal_hand(self, deck, hand_size):
        hand = []
        x = 0
        y = 0

        while y < hand_size:
            hand.append(self.deal_top_card(deck))
            y += 1
        x += 1

        return hand

    # sort the players hand from low to high value
    def sort_hand(self, hands, player):
        sorted_hand = sorted(hands[player], key=lambda x: x.value)
        return sorted_hand

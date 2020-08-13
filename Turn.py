from Card import Card
from Deck import Deck


class Turn:

    def __init__(self):
        self.deck = Deck()

    # prints players' (sorted) hand
    def see_current_hand(self, hands, player):
        sorted_hand = self.deck.sort_hand(hands, player)
        cards = []
        for x in sorted_hand:
            cards.append(x.get_full_name())
        print(cards)

    # creates list of players from dictionary keys
    def get_players(self, keys):
        player_names = list(keys)
        return player_names

    # query function
    def ask_for_card(self, hands, ask_card, player1, player2):
        p1_hand = list(hands[player1])
        p2_hand = list(hands[player2])

        # make sure card exists in the players hand
        if ask_card in p1_hand:
            crd = ask_card
        else:
            print("ERROR: card not in hand.")
            quit()

        # find indexes of card asked in both hands
        # if found,
        # add card to asker's hand
        # remove from target hand
        x = 0
        cards_taken = 0
        while x < len(p2_hand):
            if crd.rank == p2_hand[x].rank:
                hands[player1].append(p2_hand[x])
                hands[player2].remove(p2_hand[x])
                cards_taken += 1
            x += 1

        return cards_taken

    # go fish: remove from draw pile and add to player's hand
    def go_fish(self, draw_pile, hands, player):
        fished_card = self.deck.deal_top_card(draw_pile)
        hands[player].append(fished_card)
        return fished_card

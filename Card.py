import Constants


def set_value(rank):
    for x in range(1, 11):
        if rank == str(x):
            value = x
    if rank == "JACK":
        value = 11
    if rank == "QUEEN":
        value = 12
    if rank == "KING":
        value = 13
    if rank == "ACE":
        value = 14  # for Go Fish

    return value


class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

        self.value = set_value(self.rank)

    # returns the fully concatenated name of the card, e.g. ACE + of + SPADES
    def get_full_name(self):
        card = self.rank + " of " + self.suit
        return card

    # give the cards values for sorting/scoring purposes


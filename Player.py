import time
from Turn import Turn
from Card import Card
import Constants

class Player:

    def __init__(self, name, books):
        self.name = name
        self.books = books

        self.cards_asked = []

        self.turn = Turn()
        self.ranks = Constants.RANK


    def play_turn(self, hands, draw_pile, player):
        while True:
            print("")
            self.turn.see_current_hand(hands, player)
            print("")
            cards_taken = 0
            p_hand = list(hands[player])

            if len(p_hand) > 0:
                while True:
                    ask_card = input("Choose a card: ")

                    #check if card is valid
                    if ask_card in self.ranks:
                        valid_cards = [y for y in p_hand if y.rank == ask_card]
                        if not valid_cards:
                            print("ERROR: card not in hand.")
                            continue
                        break
                    else:
                        print("ERROR: not a valid card.")
                        continue
                
                ##set asked card to any of the tmp cards
                #(doesn't matter which one, we just want rank)
                crd = valid_cards[0]
                self.cards_asked.append(crd)

                table = self.turn.get_players(hands.keys())
                #can't ask yourself
                table.remove(player)

                #pick a player to ask
                while True:
                    print("")
                    print(table)
                    print("")
                    ask_player = input("Choose player: ")
                    if ask_player in table:
                        pl = ask_player
                        break
                    else:
                        print("")
                        print("Not a valid player.")
                        continue
                
                time.sleep(0.2)
                print("")
                print(pl + ", do you have any " + crd.rank + "'s?")
                
                #check if you made a catch, try to make a book
                cards_taken = self.turn.ask_for_card(hands, crd, player, pl)
                if cards_taken > 0:
                    self.books = self.create_book(hands, player, self.books)
                    continue
                else:
                    break
            else:
                print("")
                print("Hand empty!")  
                break
        
        ##check if the draw pile has cards, and draw
        #also do another check if a book can be made
        if len(draw_pile) > 0:
            fished_card = self.turn.go_fish(draw_pile, hands, player)
            self.books = self.create_book(hands, player, self.books)
            print("")
            print("Go fish!")

            time.sleep(0.2)
            print("")
            print("Draw card: ", fished_card.get_full_name())

        else:
            print("")
            print("Draw pile empty!")


    def create_book(self, hands, player, books):
        p_hand = list(hands[player])
        x = 0
        ##make a tmp book with any matching ranks in the player's hand
        #if tmp book has all four suits of that rank, remove them and add to books count
        while x < len(self.ranks):
            temp_book = [y for y in p_hand if y.rank == self.ranks[x]]
            if len(temp_book) == 4:
                books += 1
                hands[player] = [z for z in hands[player] if z not in temp_book]            
            x += 1
            temp_book = []

        return books
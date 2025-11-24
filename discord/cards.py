from random import choice

class CardPack():

    def __init__(self):
        self._card_numbers = [1,2,3,4,5,6,7,8,9,10,11,12,13]
        self._card_suits = ["♡","♢","♧","♤"]
        self._card_face = {
            1 : "A",
            11 : "K",
            12 : "Q",
            13 : "J",
            "A" : 1,
            "K" : 11,
            "Q" : 12,
            "J" : 13,
        }
        self._deck = []
    
    @property
    def card_numbers(self):
        return self._card_numbers
    
    @property
    def card_suits(self):
        return self._card_suits
    
    @property
    def card_face(self):
        return self._card_face
    
    @property
    def deck(self):
        return self._deck
    
    @property
    def is_empty(self):
        return len(self._deck) == 0

    def new_pack(self,num_packs = 1): #how many packs you want 
        self._deck = []
        for _ in range (num_packs):
            for i in self.card_suits:
                for j in self.card_numbers:
                    if j == 1 or j >= 11:
                        card = self.card_face[j] + i
                    else:
                        card = str(j) + i
                    self._deck.append(card)

    def random_pick(self,remove = True):
        if not self.deck:
            return None
        pick = choice(self.deck)
        if remove:
            self._deck.remove(pick)
        return pick

    def deal(self, num_cards=1):
        if num_cards > len(self._deck):
            return None
        hand = []
        for _ in range(num_cards):
            hand.append(self.random_pick())
        return hand

    def reset(self, num_packs=1):
        self.new_pack(num_packs)

def test_cards():
    pack1 = CardPack()
    pack1.new_pack(2) #can be empty for a defualt of 1 pack
    print(pack1.deck)

    print()
    pack1.reset() #a number maybe inputed for more packs
    print(pack1.deck)

    print()
    print(pack1.random_pick()) #removes the card (defualt True)
    print(pack1.deck)

    print()
    print(pack1.random_pick(False)) #does not remove the card
    print(pack1.deck)

    print()
    print(pack1.deal(2))
    

if __name__ == "__main__":
    test_cards()
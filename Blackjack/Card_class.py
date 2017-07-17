#!/usr/bin/python3
# Card_class.py
# arcanearronax
# 07/16/2017

import random as r


class Card:
    # This is equivalent to a blank card
    def __init__(self):
        self.face = ''
        self.suit = ''

    # Need to be able to print out the regular card name
    def __str__(self):
        if self.face == '' or self.suit == '':
            return "Blank Card"
        else:
            return self.face + " of " + self.suit

    # In case we need to see the oject itself
    def __repr__(self):
        if (self.face != '') and (self.suit != ''):
            return '(\'{}\',\'{}\')'.format(self.face, self.suit)
        else:
            return '(\'null\',\'null\')'

    # To be used when using a generator to get cards
    def convCard(face, suit):
        card = Card()

        if (face < 0 or face > 12) or (suit < 0 or suit > 3):
            raise ValueError("Card.convCard: face - " + str(face) + " : suit - " + str(suit))

        if face is 0:
            card.face = 'Ace'
        elif face > 0 and face < 10:
            card.face = str(face + 1)
        elif face is 10:
            card.face = 'Jack'
        elif face is 11:
            card.face = 'Queen'
        elif face is 12:
            card.face = 'King'

        if suit is 0:
            card.suit = 'Diamonds'
        elif suit is 1:
            card.suit = 'Clubs'
        elif suit is 2:
            card.suit = 'Spades'
        elif suit is 3:
            card.suit = 'Hearts'

        return card

    # Need a score to determine card value
    def score(self):
        if self.face in ['King', 'Queen', 'Jack']:
            return 10
        elif self.face == 'Ace':
            return 'A'
        else:
            return int(self.face)

# Going to try to build this as an iterable class
# At some point a deck is being added as a card, this kinda needs fixing...
class Shoe:
    def __init__(self, numdecks):
        self.cards = Shoe.getDeck(numdecks)

    def getDeck(numdecks):
        temp = []

        # I think this is like stuttering recursion
        # Should probably rewrite this
        while numdecks > 0:
            for i in range(12):
                for j in range(4):
                    temp.append(Card.convCard(i,j))
            numdecks -= 1
            if numdecks > 0:
                temp += Shoe.getDeck(numdecks)

        return temp

    # The cards variable is meant to be a list of Card()
    # This will reorder the list of cards using an RNG
    def shuffle(cards):
        count = len(cards)
        temp = []
        shuffled = []
        for i in range(count):
            temp.append(i)
        while len(cards) > 1:
            rand = r.randint(0, len(cards) - 1)
            shuffled.append(cards[rand])
            cards.remove(cards[rand])
        return shuffled

    # take the bottom card from the shoe/top from the deck (index 0)
    def draw(shoe):
        #print("Deck: {}".format(deck))
        card = shoe[0]
        shoe.pop(0)
        return card

#!/usr/bin/python3

####################################################################
##	BBB	  L		   A	 CCCC	K  K  JJJJJ	   A	 CCCC	K  K  ##
##	B  B  L		  A	A	C	 C	K K		J	  A A	C	 C	K K	  ##
##	BBB	  L		 A	 A	C		KK		J	 A	 A	C		KK	  ##
##	B  B  L		 AAAAA	C	 C	K K	  J J	 AAAAA	C	 C	K K	  ##
##	BBB	  LLLLL	 A	 A	 CCCC	K  K   J	 A	 A	 CCCC 	K  K  ##
####################################################################

# This is just a blackjack game from practice purposes.
# It should be able to play one player against a dealer.
import os
from Blackjack_class import *

os.system('clear')

# Instantiate BlackJack
blackjack = BlackJack()

print("Welcome to Black Jack")

# Player stuff
player = Player(input('What is your name?\n'))

# Card stuff
shoe = Card.shuffle(Card.getDeck(BlackJack.numdecks))

# Dealer and chip shit
dealer = Dealer()
BlackJack.distribChips(player)

play = True

while play is True:
	# Deal cards
	BlackJack.dealCards(shoe, player)
	BlackJack.dealCards(shoe, dealer)

	# Player moves
	player.showCards()
	blackjack.bet(player, input('What would you like to bet?\n'))

	# Determine winner

	# Keep playing
	play = False

print(player.getChipCount())
print("Player: {}".format(player.hand))
print("Dealer: {} {}".format(str(dealer.hand[0]), str(dealer.hand[1])))

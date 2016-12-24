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

print("Welcome to Black Jack")

# Initialize the House
house = House()

# Initialize the Shoe
shoe = Shoe()
shoe.stackShoe()

# Build player
dude = Player()
dude.getInfo()

# Issue chips
dude.issueChips()

play = True

while play is True:
	# Deal cards
	dude.hand.dealHand()

	# Player moves

	# Determine winner

	# Keep playing
	play = False

print(dude.name)
print(dude.hand.card1)
print(dude.hand.card2)

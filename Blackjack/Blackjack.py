#!/usr/bin/python3

# arcanearronax
# 12/24/2016

####################################################################
##	BBB	  L		   A	 CCCC	K  K  JJJJJ	   A	 CCCC	K  K  ##
##	B  B  L		  A	A	C	 C	K K		J	  A A	C	 C	K K	  ##
##	BBB	  L		 A	 A	C		KK		J	 A	 A	C		KK	  ##
##	B  B  L		 AAAAA	C	 C	K K	  J J	 AAAAA	C	 C	K K	  ##
##	BBB	  LLLLL	 A	 A	 CCCC	K  K   J	 A	 A	 CCCC 	K  K  ##
####################################################################

# This is just a blackjack game from practice purposes.
# It should be able to play one player against a dealer.
from Blackjack_class import *

# Build the game
blackjack = BlackJack()
blackjack.createPlayers()
blackjack.distribChips()

play = True

while play is True:
    # Deal cards
    blackjack.dealCards()
    blackjack.bet()

    Debug.printAllHands(blackjack)

    play = False

print(blackjack.winner)
print('Program Complete. Testing Below.')

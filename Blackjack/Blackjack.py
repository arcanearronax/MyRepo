#!/usr/bin/python3
# Blackjack.py
# arcanearronax
# 12/24/2016

########################################################################
##  BBB     L        A     CCCC   K  K   JJJJJ     A    CCCC    K  K  ##
##  B  B   L       A A   C     C  K K      J     A A   C     C  K K   ##
##  BBB    L      A  A  C         KK       J    A  A  C         KK    ##
##  B  B  L      AAAAA   C     C  K K    J J   AAAAA   C     C  K K   ##
##  BBB   LLLL  A    A    CCCC    K  K    J   A    A    CCCC    K  K  ##
########################################################################

# This is just a blackjack game from practice purposes.
# It should be able to play one player against a dealer.
from Blackjack_header import *

blackjack = BlackJack()
blackjack.distribChips()

play = True

while play is True:
    # Bet
    blackjack.bet()
    #Debug.printAttrs(blackjack)

    # Deal
    blackjack.dealCards()
    #Debug.printAttrs(blackjack)

    # Turn
    blackjack.turn()
    #Debug.printAttrs(blackjack)

    # Finish up the hand
    blackjack.winner()
    #Debug.printAttrs(blackjack)

    play = blackjack.playAgain()

print('Program Complete. Testing Below.')

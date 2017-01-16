#!/usr/bin/python3
# Blackjack.py
# arcanearronax
# 01/16/2017

########################################################################
##  BBB     L        A     CCCC   K  K   JJJJJ     A    CCCC    K  K  ##
##  B  B   L       A A   C     C  K K      J     A A   C     C  K K   ##
##  BBB    L      A  A  C         KK       J    A  A  C         KK    ##
##  B  B  L      AAAAA   C     C  K K    J J   AAAAA   C     C  K K   ##
##  BBB   LLLL  A    A    CCCC    K  K    J   A    A    CCCC    K  K  ##
########################################################################

# This is just a blackjack game that I made to practice using python and more
# specifically building classes. I plan to work on it continuously and make
# additions and changes.

# This program will create a blackjack game and cycle through the different
# parts of a blackjack game until the loop is broken.

# At this point I'm pretty sure I don't even need the header file, but I'm gonna
# keep it since it's not hurting anything.
from Blackjack_header import *

#  Start the game and set the break variable
blackjack = BlackJack()
play = True

while play is True:
    # Get the players' bets
    blackjack.bet()

    # Deal out the cards to players
    blackjack.dealCards()

    # Have the players make their moves
    blackjack.turn()

    # Figure out who wins and payout chips
    blackjack.winner()

    # Handle changing players, playing again, and exiting
    play = blackjack.playAgain()

print('Program Complete.')

#!/usr/bin/python3
# Debug_class.py
# arcanearronax
# 01/13/2017

from Blackjack_class import *
from Card_class import *
from Player_class import *
import random as r
import os

class Debug:
    # Verification stuff
    # To make sure the user input a number
    def intput(prompt):
        num = input(prompt)
        try:
            num = int(num)
            if num < 0:
                raise ValueError
        except ValueError:
            num = Debug.intput('Invalid entry. Input was not a number, please try again.\n')
        return num

    # Testing stuff
    def printAllHands(blackjack):
        for player in blackjack.players:
            print('{}: {}'.format(player.name, player.hand))
            print('{}: {}'.format('dealer', blackjack.dealer.hand))

    def spacer():
        print("#\n#\n#\n")

    def printAttrs(blackjack):
        for player in blackjack.players:
            print('--Player Info')
            print('----' + player.name)
            print('----' + str(player.chipcount))
            print('----' + str(player.hand))
            print('----' + str(player.pot))
        print('--Dealer Info')
        print('----' + blackjack.dealer.name)
        print('----' + str(blackjack.dealer.chipcount))
        print('----' + str(blackjack.dealer.hand))

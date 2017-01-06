#!/usr/bin/python3

# arcanearronax
# 12/24/2016

from Card_class import *
from Player_class import *
from Debug_class import *

import random as r
import os

# This class will contain all methods needed to write a blackjack game.
# It will handle everything dealing with other classes. Those classes can still
# be used if the writer wants more manual control over the game
class BlackJack:
    # Set up the terminal when the instance is created
    def __init__(self):
        os.system('clear')
        print('Welcome to Black Jack.')
        self.pot = 0
        # Go ahead and build these since there's not reason not to now
        self.dealer = Dealer(BlackJack.dealerchips)
        self.shoe = Shoe.shuffle(Shoe.getDeck(self.numdecks))
        self.players = BlackJack.createPlayers()

    # Values that may need to be used and modified manually
    numdecks = 4
    defaultchips = 1000
    dealerchips = 10000
    minbet = 50
    maxbet = 500

    # Values that will be modified by methods
    players = []
    shoe = []

    # Prompt for the number of player and create them sequentially
    def createPlayers():
        players = []
        # Need to have some verification to ensure the user input is an int
        for i in range(Debug.intput('How many people will be playing?\n')):
            players.append(Player(input('Player {} Name: '.format(i+1))))

        return players

    # Sets each player to the default chip count
    def distribChips(self):
        for player in self.players:
            player.chipcount = self.defaultchips

    # Deal cards out to the players and dealers
    # Should probably update the player class to have it's own draw method
    def dealCards(self):
        for i in range(2):
            for player in self.players:
                player.hand.append(Shoe.draw(self.shoe))
            self.dealer.hand.append(Shoe.draw(self.shoe))

    # This is close to working as I want, need to raise errors appropriately
    def bet(self):
        for player in self.players:
            ans = Debug.intput("{}\'s bet: ".format(player.name))
            resp =  player.isSufficient(ans, BlackJack.minbet, BlackJack.maxbet)
            while type(resp) == str:
                print(resp)
                ans = Debug.intput("{}\'s bet: ".format(player.name))
                resp =  player.isSufficient(ans, BlackJack.minbet, BlackJack.maxbet)
            player.chipcount -= ans
            player.pot += ans

    def turn(self):
        for player in self.players:
            # Get the player's score at the start of their turn
            BlackJack.getScore(player)
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            print("Score: {}".format(player.score))
            opts = BlackJack.getOpts(player)
            # The menu piece
            for i in range(len(opts)):
                if opts[i] == True:
                    if i == 0:
                        print('1. Stay')
                    if i == 1:
                        print('2. Hit')
                    if i == 2:
                        print('3. Double')
                    if i == 3:
                        print('4. Split')
            # Handle getting the player choice here
            choice = Debug.intput("Please select your move: ")
            # Check the input to see if it's valid
            while choice > len(opts) or choice < 0 or opts[choice - 1] == False:
                choice = Debug.intput("Invalid selection. Please select your move: ")
            # Make the players move
            if choice == 1:
                BlackJack.stay(player)
            elif choice == 2:
                BlackJack.hit(player)
                BlackJack.getScore(player)
                if player.score < 21:
                    contTurn(player, self.shoe)
            elif choice == 3:
                BlackJack.double(player, self.shoe)
            elif choice == 4:
                BlackJack.split(player, self.shoe)

    # This will provide a list of available player moves
    def getOpts(player):
        opts = [True,False,False,False]
        if player.score >= 21:
            opts[0] = False
        elif player.score < 21:
            opts[1] = True
            if len(player.hand) == 2:
                if player.chipcount >= player.pot:
                    opts[2] = True
                    if player.hand[0].face == player.hand[1].face:
                        opts[3] = True
        return opts

    def stay(player):
        pass

    def hit(player, shoe):
        print('HIT')

    def double(player, shoe):
        player.chipcount -= player.pot
        player.pot *= 2
        player.hand.append(Shoe.draw(shoe))
        print('DOUBLE')

    def split(player, shoe):
        print('SPLIT')

    # To be used to after the first player's move
    def contTurn(player, shoe):
        pass

    # An ace will return as 'A' rather than 11, to keep track more effectively
    def getScore(player):
        score = 0
        acount = 0
        for card in player.hand:
            temp = card.score()
            if type(temp) == str:
                acount += 1
            else:
                score += temp
        # Not sure if this would work for acount = 0
        for i in range(acount):
            if score <= 10:
                score += 11
                acount -= 1
            else:
                score += 1
                acount -= 1
        player.score = score

#
#
# check below here for functions, everything above has been verified to some degree
#
#

    # Show the cards for all players and dealer
    def displayCards(self):
        for player in self.players:
            print("{}'s Hand: {}".format(player.name, player.hand))
        # BugTracing001: dealer has decks as hands, why were they place in had?
        print("{}'s Hand: {}".format(self.dealer.name, self.dealer.hand))

    # This has each player take their turn sequentially, then the dealer. It
    # does the looping itself


    # Currently checks with the single player to see if they want to
    # play another hand
    def keepplaying(player):
        print('You have {} chips.\n'.format(player.chipcount))
        if input('Would you like to keep playing?\n') == 'y':
            return True
        else:
            return False
            print('Thank you for playing.\n')

    def winner(self):
        for player in self.players:
            player.winner()

    def revealwinners(self):
        for player in self.players:
            if player.win == 0:
                print("{}: Draw".format(player.name))
            elif player.win == 1:
                print("{}: Blackjack".format(player.name))
            elif player.win == 2:
                print("{}: Win".format(player.name))
            elif player.win == 3:
                print("{}: Lose".format(player.name))
            elif player.win == 4:
                print("{}: Bust".format(player.name))

        def score(self):
            total = 0
            acecount = 0
            for card in self.hand:
                if card.score() == 'A':
                    acecount += 1
                else:
                    total += card.score()
            # This will try to maximize the the ace contribution
            while acecount > 0:
                acecount -= 1
                if acecount + total + 11 <= 21:
                    total += 11
                else:
                    total += 1
            return total

    # win = 0 --> no winner determined/draw
    # win = 1 --> player blackjack
    # win = 2 --> player wins
    # win = 3 --> dealer wins
    def winner(self):
        #pscore = self.score()
        #dscore = self.dealer.score()
        if self.blackjack == True:
            self.win = 1
        elif self.score() > self.dealer.score():
            self.win = 2
        elif self.score() < self.dealer.score():
            self.win = 3

    def soft(self, num):
        ace = False
        for card in self.hand:
            if card.face == 'Ace':
                ace = True
                break
        if ace == True and self.score - 11 == num:
            return True
        else:
            return False

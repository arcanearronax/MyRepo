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
        # Need to show the dealer's card
        print("Dealer's hand: {}".format(str([self.dealer.hand[0], 'Blank Card'])))
        for player in self.players:
            # Get the player's score at the start of their turn
            BlackJack.getScore(player)
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            print("Score: {}".format(player.score))
            if player.score < 21:
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
                    BlackJack.hit(player, self.shoe, 0)
                    BlackJack.getScore(player)
                    if player.score < 21:
                        BlackJack.contTurn(player, self.shoe)
                    else:
                        BlackJack.printHand(player, 1)
                elif choice == 3:
                    BlackJack.double(player, self.shoe)
                elif choice == 4:
                    BlackJack.split(player, self.shoe)
                    BlackJack.contTurn(player, self.shoe)
                    BlackJack.getScore(player)
            elif player.score == 21:
                pass
        # Dealer moves now
        BlackJack.getScore(self.dealer)
        while self.dealer.score < 17:
            BlackJack.hit(self.dealer, self.shoe, 0)
            BlackJack.getScore(self.dealer)

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

    def hit(player, shoe, handopt):
        if handopt == 0:
            player.hand.append(Shoe.draw(shoe))
        elif handopt == 1:
            player.splithand.append(Shoe.draw(shoe))
        if type(player) == Player:
            print('HIT')

    # Need to check to make sure the chipcount is valid
    def double(player, shoe):
        player.chipcount -= player.pot
        player.pot *= 2
        player.hand.append(Shoe.draw(shoe))
        print("{}'s hand: {}".format(player.name, str(player.hand)))
        print('DOUBLE')

    # Need to build this so it works
    def split(player, shoe):
        player.splitpot += player.pot

        player.splithand = [player.hand[1]]
        player.hand.pop(1)
        player.hand += [Shoe.draw(shoe)]
        player.splithand += [Shoe.draw(shoe)]

        print('SPLIT')

    # To be used to after the first player's move
    def contTurn(player, shoe):
        BlackJack.getScore(player)
        while player.score < 21:
            BlackJack.printHand(player, 1)
            print("Score: {}".format(player.score))
            print('1. Stay')
            print('2. Hit')
            choice = Debug.intput("Please select your move: ")
            while choice != 1 and choice != 2:
                choice = Debug.intput("Invalid selection. Please select your move: ")
            if choice == 1:
                BlackJack.stay(player)
                break
            else:
                BlackJack.hit(player, shoe, 0)
            BlackJack.getScore(player)
        if len(player.splithand) >=2:
            while player.splitscore < 21:
                BlackJack.printHand(player, 2)
                print("Split Score: {}".format(player.splitscore))
                print('1. Stay')
                print('2. Hit')
                choice = Debug.intput("Please select your move: ")
                while choice != 1 and choice != 2:
                    choice = Debug.intput("Invalid selection. Please select your move: ")
                if choice == 1:
                    BlackJack.stay(player)
                    break
                else:
                    BlackJack.hit(player, shoe, 1)
                BlackJack.getScore(player)

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

        # Need to handle the split hand score too
        if len(player.splithand) >= 2:
            score = 0
            acount = 0
            for card in player.splithand:
                temp = card.score()
                if type(temp) == str:
                    acount += 1
                else:
                    score += temp
            for i in range(acount):
                if score <= 10:
                    score += 11
                    acount -= 1
            player.splitscore = score

    def winner(self):
        print("Dealer's Hand: {}".format(str(self.dealer.hand)))
        BlackJack.getScore(self.dealer)
        for player in self.players:
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            BlackJack.getScore(player)
            if len(player.hand) == 2 and player.score == 21:
                if self.dealer.blackjack == True:
                    print("{} breaks even 1.".format(player.name))
                    player.chipcount += player.pot
                    print("Remaining Chips: {}".format(player.chipcount))
                else:
                    print("{} wins 1.".format(player.name))
                    player.chipcount += int(player.pot * 2.5)
                    print("Remaining Chips: {}".format(player.chipcount))
            else:
                if player.score > 21:
                    print("{} loses 2.".format(player.name))
                    print("Remaining Chips: {}".format(player.chipcount))
                else:
                    if self.dealer.score > 21:
                        print("{} wins 2.".format(player.name))
                        player.chipcount += player.pot * 2
                        print("Remaining Chips: {}".format(player.chipcount))
                    elif self.dealer.score == player.score:
                        print("{} breaks even 2.".format(player.name))
                        player.chipcount += player.pot
                        print("Remaining Chips: {}".format(player.chipcount))
                    elif self.dealer.score > player.score:
                        print("{} loses 3.".format(player.name))
                        print("Remaining Chips: {}".format(player.chipcount))
                    else:
                        print("{} wins 4.".format(player.name))
                        player.chipcount += player.pot * 2
                        print("Remaining Chips: {}".format(player.chipcount))
            player.pot = 0

    def payout(self, player):
        if player.win == False:
            self.dealer.chipcount += player.pot
            player.pot = 0
        else:
            # Pick up here
            if player.blackjack == True:
                if self.dealer.blackjack == True:
                    player.chipcount += player.pot
                else:
                    player.chipcount += int(player.pot * 1.5)
            else:
                if self.dealer.blackjack == True:
                    self.dealer.chipcount += player.pot
                    player.pot = 0
                else:
                    if player.score > 21:
                        if self.dealer.score > 21:
                            player.pot = 0
                        else:
                            self.dealer.chipcount += player.pot
                            player.pot = 0
                    else:
                        if self.dealer.score > 21:
                            player.chipcount += player.pot * 2
                            player.pot = 0
                        elif self.dealer.score > player.score:
                            self.dealer.chipcount += player.pot
                        else:
                            player.chipcount += player.pot * 2
                            player.pot = 0

    def playAgain(self):
        # Kick any players who are broke
        for player in self.players:
            if player.chipcount == 0:
                print("{} is broke. Please leave the table.".format(player.name))
                self.players.remove(player)
        # Need a menu here
        print('Please select an option')
        print('1. Keep Playing')
        print('2. Reset Players')
        print('3. Quit Game')
        choice = Debug.intput('')

        # Clear the players' hands
        for player in self.players:
            player.hand = []
            player.splithand = []
        self.dealer.hand = []

        # Handle the player's choice here
        if choice == 1:
            play = True
            if len(self.players) == 0:
                choice = 2
        if choice == 2:
            self.players = BlackJack.createPlayers()
            self.distribChips()
            play = True
        elif choice == 3:
            play = False
            print ('Thanks for playing.')
        return play

    def printHand(player, selection):
        if selection == 0:
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            print("{}'s split hand: {}".format(player.name, str(player.splithand)))
        if selection == 1:
            print("{}'s hand: {}".format(player.name, str(player.hand)))
        if selection == 2:
            print("{}'s split hand: {}".format(player.name, str(player.splithand)))

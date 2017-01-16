#!/usr/bin/python3
# Blackjack_class.py
# arcanearronax
# 01/13/2017

# Need these in order to play the game and have some debugging abilities.
from Card_class import *
from Player_class import *
from Debug_class import *

# This class represents a game of blackjack. A small handful of instance methods
# are used to allow a program to run the game.
class BlackJack:
    # Putting these here for easy access to make game changes.
    numdecks = 4
    defaultchips = 1000
    dealerchips = 10000
    minbet = 50
    maxbet = 500

    # Set up the game when the class is instantiated
    def __init__(self):
        # os is imported from Debug_class
        os.system('clear')
        print('Welcome to Black Jack.')

        # Build the necessary game pieces and hand out chips
        self.dealer = Dealer(BlackJack.dealerchips)
        self.shoe = Shoe.shuffle(Shoe.getDeck(self.numdecks))
        self.players = BlackJack.createPlayers()
        self.distribChips()

################################################################################
##################### Methods to be called to run the game #####################
################################################################################

    # Get bets from the players
    def bet(self):
        for player in self.players:
            # Get the player's bet and check to see if it's valid
            ans = Debug.intput("{}\'s bet: ".format(player.name))
            resp =  player.isSufficient(ans, BlackJack.minbet, BlackJack.maxbet)
            # This check is here to get a new entry is needed, review above
            while type(resp) == str:
                print(resp)
                ans = Debug.intput("{}\'s bet: ".format(player.name))
                resp =  player.isSufficient(ans, BlackJack.minbet, BlackJack.maxbet)
            # Make the necessary modifications to the player
            player.chipcount -= ans
            player.pot += ans

    # Deal cards to player(s) and dealer
    def dealCards(self):
        for i in range(2):
            for player in self.players:
                player.hand.append(Shoe.draw(self.shoe))
            self.dealer.hand.append(Shoe.draw(self.shoe))

    # This will handle players' and the dealer's moves
    def turn(self):
        # Show the dealer's hand first
        print("Dealer's hand: {}".format(str([self.dealer.hand[0], 'Blank Card'])))
        # Cycle through each of the players
        for player in self.players:
            # Display the player's hand and give their score
            BlackJack.getScore(player)
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            print("Score: {}".format(player.score))
            # If the player doesn't have blackjack, do this stuff
            if player.score < 21:
                # Determine available player moves and print them out
                opts = BlackJack.getOpts(player)
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
                # Get the player's move and make sure it's valid
                choice = Debug.intput("Please select your move: ")
                while choice > len(opts) or choice < 0 or opts[choice - 1] == False:
                    choice = Debug.intput("Invalid selection. Please select your move: ")
                # Make the player's move
                if choice == 1:
                    BlackJack.stay(player)
                elif choice == 2:
                    BlackJack.hit(player, self.shoe, 0)
                    # Determine what the player can do after their new card
                    BlackJack.getScore(player)
                    if player.score < 21:
                        BlackJack.contTurn(player, self.shoe)
                    else:
                        # Print the player's hand if they busted
                        BlackJack.printHand(player, 1)
                elif choice == 3:
                    BlackJack.double(player, self.shoe)
                elif choice == 4:
                    # Split the player's hand
                    BlackJack.split(player, self.shoe)
                    BlackJack.contTurn(player, self.shoe)
                # Go ahead and finish by making sure the player score is updated
                BlackJack.getScore(player)
            # Don't need to do anything more if the player has blackjack
            elif player.score == 21:
                pass
        # Dealer hits until their score is > 17
        BlackJack.getScore(self.dealer)
        while self.dealer.score < 17:
            BlackJack.hit(self.dealer, self.shoe, 0)
            BlackJack.getScore(self.dealer)

    # Determine who the winner of the game is and set chips accordingly
    def winner(self):
        # Reveal what the dealer ended up with and check the dealer's score
        print("Dealer's Hand: {}".format(str(self.dealer.hand)))
        BlackJack.getScore(self.dealer)
        # Cycle through the players and finish the hands accordingly
        for player in self.players:
            # Remind them of their hand and verify their score
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            BlackJack.getScore(player)
            if len(player.hand) == 2 and player.score == 21:
                if self.dealer.blackjack == True:
                    # Dealer and player both have blackjack
                    print("{} breaks even.".format(player.name))
                    player.chipcount += player.pot
                    print("Remaining Chips: {}".format(player.chipcount))
                else:
                    # Player has blackjack and dealer doesn't
                    print("{} wins 1.".format(player.name))
                    player.chipcount += int(player.pot * 2.5)
                    print("Remaining Chips: {}".format(player.chipcount))
            else:
                if player.score > 21:
                    # Player busts, regardless of dealer's hand
                    print("{} loses 2.".format(player.name))
                    print("Remaining Chips: {}".format(player.chipcount))
                else:
                    if self.dealer.score > 21:
                        # Player < 21 and dealer busts
                        print("{} wins 2.".format(player.name))
                        player.chipcount += player.pot * 2
                        print("Remaining Chips: {}".format(player.chipcount))
                    elif self.dealer.score == player.score:
                        # Player and dealer are tied and no bust
                        print("{} breaks even 2.".format(player.name))
                        player.chipcount += player.pot
                        print("Remaining Chips: {}".format(player.chipcount))
                    elif self.dealer.score > player.score:
                        # Dealer's score is higher and no bust
                        print("{} loses 3.".format(player.name))
                        print("Remaining Chips: {}".format(player.chipcount))
                    else:
                        # Player's score higher and no bust
                        print("{} wins 4.".format(player.name))
                        player.chipcount += player.pot * 2
                        print("Remaining Chips: {}".format(player.chipcount))

            # Need to handle the split hand
            if player.splitpot != 0:
                if len(player.splithand) == 2 and player.splitscore == 21:
                    if self.dealer.blackjack == True:
                        # Dealer and player both have blackjack
                        print("{} breaks even..".format(player.name))
                        player.chipcount += player.splitpot
                        print("Remaining Chips: {}".format(player.chipcount))
                    else:
                        # Player has blackjack and dealer doesn't
                        print("{} wins 1..".format(player.name))
                        player.chipcount += int(player.splitpot * 2.5)
                        print("Remaining Chips: {}".format(player.chipcount))
                else:
                    if player.splitscore > 21:
                        # Player busts, regardless of dealer's hand
                        print("{} loses 2..".format(player.name))
                        print("Remaining Chips:     {}".format(player.chipcount))
                    else:
                        if self.dealer.score > 21:
                            # Player < 21 and dealer busts
                            print("{} wins 2..".format(player.name))
                            player.chipcount += player.splitpot * 2
                            print("Remaining Chips:    {} ".format(player.chipcount))
                        elif self.dealer.score == player.splitscore:
                            # Player and dealer are tied and no bust
                            print("{} breaks even 2..".format(player.name))
                            player.chipcount += player.splitpot
                            print("Remaining Chips:     {}".format(player.chipcount))
                        elif self.dealer.score > player.splitscore:
                            # Dealer's score is higher and no bust
                            print("{} loses 3..".format(player.name))
                            print("Remaining Chips: {}".format(player.chipcount))
                        else:
                            # Player's score higher and no bust
                            print("{} wins 4..".format(player.name))
                            player.chipcount += player.splitpot * 2
                            print("Remaining Chips: {}".format(player.chipcount))
            # Go ahead and clear pots since they're not needed
            player.pot = 0
            player.splitpot = 0

            # Clear everyone's hands
            for player in self.players:
                player.hand = []
                player.splithand = []
            self.dealer.hand = []

    # Return a boolean to determine if the game should continue
    def playAgain(self):
        # Kick any players who are broke
        for player in self.players:
            if player.chipcount == 0:
                print("{} is broke. Please leave the table.".format(player.name))
                self.players.remove(player)

        # Present the game options and get the player choice, need to verify
        print('Please select an option')
        print('1. Keep Playing')
        print('2. Reset Players')
        print('3. Quit Game')
        choice = Debug.intput('')

        # Handle the player's choice here
        if choice == 1:
            play = True
            # If no players are left, go through player creation
            if len(self.players) == 0:
                choice = 2
        if choice == 2:
            self.players = BlackJack.createPlayers()
            self.distribChips()
            play = True
        elif choice == 3:
            play = False
            print ('Thanks for playing.')
        # Return the boolean value
        return play

################################################################################
######################## Methods for building  the game ########################
################################################################################

    # Prompt for the number of player and create them sequentially
    def createPlayers():
        # Build a list of players and return it
        players = []
        for i in range(Debug.intput('How many people will be playing?\n')):
            players.append(Player(input('Player {} Name: '.format(i+1))))
        return players

    # Sets each player to the default chip count
    def distribChips(self):
        for player in self.players:
            # Use the defaultchips variable to start players off
            player.chipcount = self.defaultchips

################################################################################
############################# Methods  for players #############################
################################################################################

    # This will return a list of available player moves
    # [{Stay},{Hit},{Double},{Split}]
    def getOpts(player):
        # Stay will always be permitted
        opts = [True,False,False,False]
        if player.score < 21:
            # Hit is a valid option is score < 21
            opts[1] = True
            if len(player.hand) == 2:
                if player.chipcount >= player.pot:
                    # Double is valid if the player has enough chips and only
                    # two cards
                    opts[2] = True
                    if player.hand[0].face == player.hand[1].face:
                        # If all the above and cards' faces are equal, then
                        # split is a valid option
                        opts[3] = True
        return opts

    # If the player wants to end their turn
    def stay(player):
        # Seriously...
        pass

    # If the player wants another card
    # handopt allows this to hand split hands
    def hit(player, shoe, handopt):
        # Hit for the first hand
        if handopt == 0:
            player.hand.append(Shoe.draw(shoe))
        # Hit for the split hand
        elif handopt == 1:
            player.splithand.append(Shoe.draw(shoe))
        # This serves no significant purpose, but I like it
        if type(player) == Player:
            print('HIT')

    # If the player wants to double
    def double(player, shoe):
        # Get the player's chips and give them a card
        player.chipcount -= player.pot
        player.pot *= 2
        player.hand.append(Shoe.draw(shoe))
        print("{}'s hand: {}".format(player.name, str(player.hand)))
        # I see no need for it, but I'm keeping it
        print('DOUBLE')

    # If the player wants to split their hand
    def split(player, shoe):
        # Get the additional chips from the player
        player.splitpot += player.pot
        player.chipcount -= player.pot

        # Create the new hand and deal the new cards
        player.splithand = [player.hand[1]]
        player.hand.pop(1)
        player.hand += [Shoe.draw(shoe)]
        player.splithand += [Shoe.draw(shoe)]

        # No purpose, keeping it anyway
        print('SPLIT')

    # Used if the player can perform an additional action, should work on
    # eliminating the need for this.
    def contTurn(player, shoe):
        # If the player's score < 21 allow them to hit
        BlackJack.getScore(player)
        while player.score < 21:
            # Print the player's first hand, always should happen
            BlackJack.printHand(player, 1)
            print("Score: {}".format(player.score))
            print('1. Stay')
            print('2. Hit')
            # Get the player's choice and make sure it's valid
            choice = Debug.intput("Please select your move: ")
            while choice != 1 and choice != 2:
                choice = Debug.intput("Invalid selection. Please select your move: ")
            if choice == 1:
                BlackJack.stay(player)
                break
            else:
                # 0 will hit the normal hand
                BlackJack.hit(player, shoe, 0)
            BlackJack.getScore(player)
        # If there are at least 2 cards in split hand, then a split occurred
        if len(player.splithand) >=2:
            # If this isn't blackjack, then the player needs to make choices
            while player.splitscore < 21:
                # Show the split hand and choices
                BlackJack.printHand(player, 2)
                print("Split Score: {}".format(player.splitscore))
                print('1. Stay')
                print('2. Hit')
                # Get the player's move and validate it
                choice = Debug.intput("Please select your move: ")
                while choice != 1 and choice != 2:
                    choice = Debug.intput("Invalid selection. Please select your move: ")
                if choice == 1:
                    BlackJack.stay(player)
                    break
                else:
                    # 1 will hit the split hand
                    BlackJack.hit(player, shoe, 1)
                # Update the player's score
                BlackJack.getScore(player)

    # This will set player.score and attempt to maximize aces
    def getScore(player):
        # Keep track of aces seperately first
        score = 0
        acount = 0
        for card in player.hand:
            temp = card.score()
            # Only an ace will have a string type score, int for any other card
            if type(temp) == str:
                acount += 1
            else:
                score += temp
        # Need to convert acount to score, temp var to run the appropriate
        # number of times
        temp = acount
        for i in range(temp):
            # Need to see if all soft aces would bust the player
            if score + acount > 21:
                player.score = score + acount
            # If attempt to maximize the player's score
            elif score + acount <= 11:
                score += 11
                acount -= 1
            else:
                score += 1
                acount -= 1
        # End this by setting the player's score
        player.score = score

        # Need to handle the split hand score too
        # Does the same basic thing as above, should probably add a control
        # variable
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

    # Make it easier to print player's hand(s) and controlable too
    def printHand(player, selection):
        if selection == 0:
            print("{}'s hand: {}".format(player.name, str(player.hand)))
            print("{}'s split hand: {}".format(player.name, str(player.splithand)))
        if selection == 1:
            print("{}'s hand: {}".format(player.name, str(player.hand)))
        if selection == 2:
            print("{}'s split hand: {}".format(player.name, str(player.splithand)))

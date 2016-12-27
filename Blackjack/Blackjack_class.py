#!/usr/bin/python3

# arcanearronax
# 12/24/2016

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
		self.dealer = Dealer()
		self.shoe = Card.shuffle(Card.getDeck(self.numdecks))

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
	def createPlayers(self):
		print('How many people will be playing?')
		# Need to have some verification to ensure the user input is an int
		for i in range(int(input())):
			self.players.append(Player(input('Player {} Name: '.format(i+1))))

	# Deal cards out to the players and dealers
	# Should probably update the player class to have it's own draw method
	def dealCards(self):
		for i in range(2):
			for player in self.players:
				player.hand.append(Card.draw(self.shoe))
			self.dealer.hand.append(Card.draw(self.shoe))

	# Sets each player to the default chip count
	def distribChips(self):
		for player in self.players:
			player.chipcount = self.defaultchips

	# This is close to working as I want, need to raise errors appropriately
	def executeBet(player):
		ans = input(("{}\'s bet: ".format(player.name)))
		try:
			chips = int(ans)
			if player.chipcount >= chips:
				player.pot += chips
				player.chipcount -= chips
			else:
				print('Insufficient chips to place bet')
				BlackJack.executeBet(player)
		except ValueError:
			print("Invalid input. Please try again.")
			BlackJack.executeBet(player)

	# Show the cards for all players and dealer
	def displayCards(self):
		for player in self.players:
			print("{}'s Hand: {}".format(player.name, player.hand))
		print("{}'s Hand: {}".format(self.dealer.name, self.dealer.hand))

	# This currently checks winner as player vs dealer but should do
	# blackjack.dealer vs blackjack.players
	# This will most likely have to move to the Player class
	def winner(self, dealer, player):
		if dealer.didbust() and player.didbust():
			self.winner = Player.bust()
		elif dealer.didbust():
			self.winner = player
		elif player.didbust():
			self.winner = dealer
		elif player.score() > dealer.score():
			self.winner = player
		elif player.score() < dealer.score():
			self.winner = dealer
		else:
			self.winner = Player.draw()
		print('{} is the winner.'.format(self.winner))

	# This has each player take their turn sequentially, then the dealer. It
	# does the looping itself
	def turn(self):
		for player in self.players:
			BlackJack.executeBet(player)
			player.turn(self)

	# Currently checks with the single player to see if they want to
	# play another hand
	def keepplaying(player):
		print('You have {} chips.\n'.format(player.chipcount))
		if input('Would you like to keep playing?\n') == 'y':
			return True
		else:
			return False
			print('Thank you for playing.\n')

# Contains card attributes and mathods for handling the object
class Card:
	# This is equivalent to a blank card
	def __init__(self):
		self.face = ''
		self.suit = ''

	# Need to be able to print out the regular card name
	def __str__(self):
		if self.face is '' or self.suit is '':
			return "blank"
		else:
			return self.face + " of " + self.suit

	# In case we need to see the oject itself
	def __repr__(self):
		return '({},{})'.format(self.face, self.suit)

	# To be used when using a generator to get cards
	def convCard(face, suit):
		card = Card()

		if face is 0:
			card.face = 'Ace'
		elif face > 0 and face < 10:
			card.face = str(face)
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

	# Generate a list of cards as if they were decks from packs
	def getDeck(numdecks):
		temp = []

		# I think this is like stuttering recursion
		# Should probably rewrite this
		while numdecks > 0:
			for i in range(13):
				for j in range(4):
					temp.append(Card.convCard(i,j))
			numdecks -= 1
			if numdecks > 0:
				temp.append(Card.getDeck(numdecks))

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
	def draw(deck):
		#print("Deck: {}".format(deck))
		card = deck[0]
		deck.pop(0)
		return card

# This class contains player variables and related functions
class Player(BlackJack):
	# Require the player's name be provided when creating the player
	def __init__(self, name):
		self.name = name
		self.chipcount = 0
		self.hand = []
		self.splithand = []
		self.winner = False
		self.pot = 0
		self.nomove = True

	# Just return the player's name
	def __str__(self):
		return self.name

	# Print out the player's attribute values as a set of coordinates
	def __repr__(self):
		return "({},{},{})".format(self.name, self.chipcount, self.hand)

	# Return the player's chipcount
	def getChipCount(self):
		return self.chipcount

	# Print the player's cards to the terminal
	def showCards(self):
		print("{}: {} {}".format(self.name, self.hand[0], self.hand[1]))

	# Return a player with the name BUST
	def bust():
		return Player.__init__(Player, 'BUST')

	# Return a player with the name DRAW
	def draw():
		return Player.__init__(Player, 'DRAW')

	# Calculate the player's score
	def score(player):
		total = 0
		for card in player.hand:
			if card.face in ['King', 'Queen', 'Jack']:
				total += 10
			else:
				try:
					total += int(card)
				except TypeError:
					if card == 'Ace':
						if total > 11:
							total += 1
						else:
							total += 11
		return total

	# Seriously...
	def stay(self):
		pass

	# Need to fix this up a bit more
	def hit(self, blackjack):
		self.nomove = False
		self.hand.append(Card.draw(blackjack.shoe))

	# This needs to have more validation built into it
	def double(self, blackjack):
		# Need to raise an error if user has insufficient chips
		if self.pot > self.chipcount:
			# Need to raise an error here
			pass
		else:
			self.chipcount -= self.pot
			self.pot *= 2
			self.nomove = False
			self.hand.append(Card.draw(blackjack.shoe))

	def split(self, blackjack):
		if self.pot > self.chipcount:
			# Need to raise an error here
			pass
		else:
			self.splithand.append(self.hand[1])
			self.hand.pop(1)
			self.hand.append(Card.draw(blackjack.shoe))
			self.splithand.append(Card.draw(blackjack.shoe))

	# Needs more verification built into it
	def getOpts(self):
		opts = [1,0,0,0]
		if self.nomove == True:
			opts[2] = 1
			if self.hand[0].face == self.hand[1]:
				opts[3] = 1
		if self.score() < 21:
			opts[1] = 1
		return opts

	# May modify how I handle the available options, this doesn't feel great
	def turn(self, blackjack):
		opts = self.getOpts()
		for i in range(len(opts)):
			if opts[i] == 1:
				if i == 0:
					print('1. Stay')
				if i == 1:
					print('2. Hit')
				if i == 2:
					print('3. Double')
				if i == 3:
					print('4. Split')
		choice = Debug.intput(input('Please enter your selection.\n'))
		if choice == 1:
			self.stay()
		if choice == 2:
			self.hit(blackjack)
		if choice == 3:
			self.double(blackjack)
		if choice == 4:
			self.split(blackjack)

# Dealer should be created with the same info repeatedly, subclass it
class Dealer(Player):
	# Automatically build the dealer
	def __init__(self):
		Player.__init__(self, 'Dealer')
		self.chipcount = BlackJack.dealerchips

	# Reveal the dealer's face down card
	def reveal(self, shoe):
		self.hand[1] = Card.draw(shoe)

	# The dealer will need their own turn method
	def turn(self):
		pass

# Methods that could be useful for testing and debugging
class Debug:
	# Verification stuff
	# To make sure the user input a number
	def intput(num):
		try:
			num = int(num)
		except ValueError:
			num = Debug.intput(input('Invalid entry. Input was not a number, please try again.\n'))
		return num

	# Testing stuff
	def printAllHands(blackjack):
		for player in blackjack.players:
			print('{}: {}'.format(player.name, player.hand))
		print('{}: {}'.format('dealer', blackjack.dealer.hand))

#!/usr/bin/python3

# arcanearronax
# 12/24/2016

import random as r
import os

# This is the class file for the blackjack program
# It will manage methods that require unrelated classes
class BlackJack:

	# Set up the terminal when the class is instantiated
	def __init__(self):
		os.system('clear')
		print('Welcome to Black Jack.')
		self.pot = 0
		self.dealer = Dealer()
		self.shoe = Card.shuffle(Card.getDeck(self.numdecks))

	# Values that may need to be used and modified manually
	numdecks = 4
	defaultchips = 1000
	dealerchips = 10000
	smallblind = 50
	largeblind = 100
	minbet = 50
	maxbet = 500

	# Values that will be modified by methods
	players = []
	shoe = []
	blindindex = 0

	# Currently the adds a single player, but it should prompt for a
	# specific number of players, then create them
	def createPlayers(self):
		print('How many people will be playing?')
		for i in range(int(input())):
			self.players.append(Player(input('Player {} Name: '.format(i+1))))

	# Remove a card from shoe and give it to player
	def dealCards(self):
		for i in range(2):
			for player in self.players:
				player.hand.append(Card.draw(self.shoe))
			self.dealer.hand.append(Card.draw(self.shoe))

	# Currently gives the solo player chips, but should give multiple
	# players chips.
	def distribChips(self):
		for player in self.players:
			player.chipcount = self.defaultchips

	# This currently does not make any checks to see if the bet amount
	# is valid, but it should do so and raise errors appropriately
	def bet(self):
		for player in self.players:
			try:
				chips = int(input(("{}\'s bet: ".format(player.name))))
			except TypeError:
				print("Invalid input. Please try again.")
				bet(self)

	# This currently checks winner as player vs dealer but should do
	# blackjack.dealer vs blackjack.players
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

	# Currently prompts the single user for a turn but should prompt
	# blackjack.players sequentially
	def turn(self, player, shoe):
		self.bet(player, input('What would you like to bet?\n'))
		cont = True
		while cont == True:
			print('Player hand: {}'.format(player.hand))
			if input('Would you like another card?\n') == 'y':
				player.hand.append(Card.draw(shoe))
			else: cont = False

	# Currently checks with the single player to see if they want to
	# play another hand
	def keepplaying(player):
		print('You have {} chips.\n'.format(player.chipcount))
		if input('Would you like to keep playing?\n') == 'y':
			return True
		else:
			return False
			print('Thank you for playing.\n')

	# Check to see if the player's score is over 21
	def didbust(player):
		if player.score() > 21:
			return True
		else:
			return False

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

		#print(temp)

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
			#print("length: {}".format(len(cards)))
			rand = r.randint(0, len(cards) - 1)
			#print(rand)
			shuffled.append(cards[rand])
			cards.remove(cards[rand])

		return shuffled

	# take the bottom card from the shoe/top from the deck (index 0)
	def draw(deck):
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
		self.winner = False
		self.pot = 0

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

# Dealer should be created with the same info repeatedly, subclass it
class Dealer(Player):
	# Automatically build the dealer
	def __init__(self):
		Player.__init__(self, 'Dealer')
		self.chipcount = BlackJack.dealerchips

	# Reveal the dealer's face down card
	def reveal(self, shoe):
		self.hand[1] = Card.draw(shoe)

# Methods that could be useful for testing and debugging
class Debug:
	def printAllHands(blackjack):
		for player in blackjack.players:
			print('{}: {}'.format(player.name, player.hand))
		print('{}: {}'.format('dealer', blackjack.dealer.hand))

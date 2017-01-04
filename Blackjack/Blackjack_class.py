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
			ans = intput(("{}\'s bet: ".format(player.name)))
			while isSufficient(ans) != True:
				print('Your chipcount is insufficient. Please bet again.')
				ans = intput(("{}\'s bet: ".format(player.name)))

			player.chipcount -= ans
			player.pot += ans

# check below here for functions, everything above has been verified to some degree

	# Show the cards for all players and dealer
	def displayCards(self):
		for player in self.players:
			print("{}'s Hand: {}".format(player.name, player.hand))
		# BugTracing001: dealer has decks as hands, why were they place in had?
		print("{}'s Hand: {}".format(self.dealer.name, self.dealer.hand))

	# This has each player take their turn sequentially, then the dealer. It
	# does the looping itself
	def turn(self):
		for player in self.players:
			print("Score: {}".format(player.score()))
			player.turn(self.shoe)
			# Need to see if player wants another card
			print("{}'s Hand: {}".format(player.name, player.hand))
			while player.score() < 21 :
				print("Score1: {}".format(player.score()))
				print('1. Stay')
				print('2. Hit')
				choice = Debug.intput(input('Please enter your selection.\n'))
				if choice == 1:
					break
				if choice == 2:
					player.hit(shoe)
		self.dealer.turn(self.shoe)

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

	# Figured out a use for this
	def stay(self):
		self.done = True

	# Need to fix this up a bit more
	def hit(self, shoe):
		self.nomove = False
		self.hand.append(Card.draw(shoe))

	# This needs to have more validation built into it
	def double(self, shoe):
		self.nomove = False
		# Need to raise an error if user has insufficient chips
		if self.pot > self.chipcount:
			# Need to raise an error here
			pass
		else:
			self.chipcount -= self.pot
			self.pot *= 2
			self.hand.append(Card.draw(blackjack.shoe))

	def split(self, shoe):
		self.nomove = False
		if self.pot > self.chipcount:
			# Need to raise an error here
			pass
		else:
			self.splithand.append(self.hand[1])
			self.hand.pop(1)
			self.hand.append(Card.draw(shoe))
			self.splithand.append(Card.draw(shoe))

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

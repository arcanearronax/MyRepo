#!/usr/bin/python3
# Player_class.py
# arcanearronax
# This class contains player variables and related functions

class Player:
	# Require the player's name be provided when creating the player
	def __init__(self, name):
		self.name = name
		self.chipcount = 0
		self.hand = []
		self.splithand = []

		self.win = 0
		self.pot = 0
		self.cont = True
		self.blackjack = False
		self.done = False

	# Just return the player's name
	def __str__(self):
		return self.name

	# Print out the player's attribute values as a set of coordinates
	def __repr__(self):
		return "({},{},{})".format(self.name, self.chipcount, self.hand, self.splithand, self.win, self.pot, self.cont, self.blackjack, self.done)

# Dealer should be created with the same info repeatedly, subclass it
class Dealer(Player):
	# Automatically build the dealer
	def __init__(self, chips):
		Player.__init__(self, 'Dealer')
		self.chipcount = chips

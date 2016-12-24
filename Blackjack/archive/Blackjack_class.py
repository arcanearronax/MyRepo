#!/usr/bin/python3
import random

# This is the class file for the blackjack program
class BlackJack:
	
	# Values that may need to be used by other programs
	numdecks = 4
	defaultchips = 1000
	smallblind = 50
	largeblind = 100
	minbet = 50
	maxbet = 500

# This class contains player variables and related functions
	class Player:
		# This holds player information
		def __init__(self):
			self.name = ''
			self.chipcount = 0
			self.hand = Hand()
	
		# This gets the player information
		def getInfo(self):
			self.name = input("What is your name: ")
		
		def issueChips(self):
			self.chipcount = BlackJack.defaultchips
	
		# This will hold a player's cards
		class Hand:
			# This will create a new hand of cards
			def __init__(self):
				self.card1 = Card()
				self.card2 = Card()
				#print("My hand here")
		
			def dealHand(self):
				self.card1 = Card.newCard()
				#print(self.card1)
				self.card2 = Card.newCard()
				#print(self.card2)
	
	class Card:
		# Values of the card's traits
		def __init__(self):
			suit = ''
			face = ''
			#print("My card here")
		
		def __str__(self):
			return self.face + " of " + self.suit
		
		def newCard():
			return Card.convCard(random.randint(0, 3), random.randint(0, 12))
	
		def convCard(suit, num):
			# This might not work...
			output = Card()
			
			print("{}	{}".format(suit, num))
	
			# Find the suit
			if suit is 0:
				output.suit = 'Diamonds'
			elif suit is 1:
				output.suit = 'Spades'
			elif suit is 2:
				output.suit = 'Clubs'
			elif suit is 3:
				output.suit = 'Hearts'
	
			# Set the number
			# Little bit of a cop out right now
			if num is 0:
				output.face = 'Ace'
			elif num > 0 and num < 10:
				output.face = str(num + 1)
			elif num is 10:
				output.face = 'Jack'
			elif num is 11:
				output.face = 'Queen'
			elif num is 12:
				output.face = 'King'
			
			return output

	# Need to rebuild this class so
	# it contains a set of Card objects
	# rather than just a 2D array
	class Deck:
		def __init__(self):
			self = []
			cur = 0
			move = 0

		def __iter__(self):
			return self

		def __next__(self):
			if cur < move:
				
		def count(self):
			count = 0
			<F12>
			
		# Need to actually make this
		def buildDeck(self):
			for i in range(52):
				pass
	
	class Shoe:
		def __init__(self):
			self = []
	
		def stackShoe(self):
			self = BlackJack.Deck()
	
			print(self)
	
			for i in range(BlackJack.numdecks):
				BlackJack.Deck.addDeck(self)
		
		# This won't work properly early on, the probability
		# of cards will not be weighted, they will only be
		# based on an rng
		def dealCard(self):
			remains = BlackJack.Shoe()
			# create a list of coordinates with values > 0
			# and use an rng to pick the list item, then
			# decode the card and handle the ops
			for i in range(4):
				col = 0
				for j in range(13):
					if shoe[j][i] is not 0:
						remains.append(col * 13 + j)
			
			pick = random.randint(0, remains.length())
	
			return BlackJack.Card.convCard((pick % 13), (pick / 13))
	
	class House:
		def __init__(self):
			bank = 1000000
			pot = 0
			sidepot = 0
	
		def bet(self, player):
	
			print("You currently have {} chips. How many would you like to bet?".format(player.chipcount))
			chips = int(input())
	
			remain = player.chipcount - chips 
			if remain >= 0:
				player.chipcount -= chips
				self.pot = chips
		
	
	

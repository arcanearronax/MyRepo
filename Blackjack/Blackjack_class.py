#!/usr/bin/python3

# arcanearronax
# 12/24/2016
 
import random as r

# This is the class file for the blackjack program
class BlackJack:
	
	# Values that may need to be used by other programs
	numdecks = 4
	defaultchips = 1000
	dealerchips = 10000
	smallblind = 50
	largeblind = 100
	minbet = 50
	maxbet = 500

	pot = 0
	winner = ''

	def dealCards(shoe, player):
		player.hand.append(shoe[0])
		if type(player) == Player:
			player.hand.append(shoe[1])
		else:
			player.hand.append(Card())
		shoe.pop(0)
		shoe.pop(1)

	def distribChips(player):
		player.chipcount = BlackJack.defaultchips

	def bet(self, player, temp):
		chips = int(temp)
		self.pot = self.pot + chips
		player.chipcount -= chips

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

# Hopefully this time the cards will fucking work...
class Card:
	def __init__(self):
		self.face = ''
		self.suit = ''

	def __str__(self):
		if self.face is '' or self.suit is '':
			return "blank"
		else:
			return self.face + " of " + self.suit
	
	def __repr__(self):
		return '({},{})'.format(self.face, self.suit)
	
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
		
	def draw(deck):
		card = deck[0]
		deck.pop(0)
		return card
		
# This class contains player variables and related functions
class Player(BlackJack):
	def __init__(self, name):
		self.name = name
		self.chipcount = 0
		self.hand = []

	def __str__(self):
		return self.name

	def __repr__(self):
		return "({},{})".format(self.name, self.chipcount)

	def setName(self, name):
		self.name = name

	def getName(self):
		return self.name

	def getChipCount(self):
		return self.chipcount
	
	def newPlayer(name, chipcount):
		temp = Player()
		temp.name = name
		temp.chipcount = chipcount
		return temp

	def showCards(self):
		print("Player: {} {}".format(self.hand[0], self.hand[1]))

	def didbust(self):
		if self.score() > 21:
			return True
		else:
			return False

	def bust():
		return Player.__init__(Player, 'BUST')

	def draw():
		return Player.__init__(Player, 'DRAW')

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

class Dealer(Player):
	def __init__(self):
		Player.__init__(self, 'Dealer')
		self.chipcount = BlackJack.dealerchips

	def reveal(self, shoe):
		self.hand[1] = Card.draw(shoe)

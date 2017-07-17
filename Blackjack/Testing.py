#!/usr/bin/python3
# Blackjack.py
# arcanearronax
# 07/16/2017

# Time to go through and work on debugging completely.\
from Blackjack_header import *

# Define the

def newCardNotNull():
    print("NewCardNotNull Test:")
    card = Card()
    if card.face != '' or card.suit != '':
        print("\tNewCardNotNull Test Failed\t- face: " + str(card.face) + " - suit: " + str(card.suit))
    else:
        print("\tNewCardNotNull Test Passed\t+")

def cardToString():
    print("CardToString Test:")
    card = Card()
    if str(card) != 'Blank Card':
        print("\tCardToString Test Failed\t- card: " + str(card))
    else:
        print("\tCardToString Test Passed\t+")

def checkScore():
    def checkScorePass(face):
        print("\tCheckScore Test Passed\t+ " + str(face))

    def checkScoreFail(card):
        print("\tCheckScore Test Failed\t- face: " + str(card.face) + " - score: " + str(card.score()))

    print("CheckScore Test:")
    # Let's get some arrays and automate this
    faces = ['Ace','1','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
    scores = ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 10]
    card = Card()
    for i in range(len(faces)):
        card.face = faces[i]
        if card.score() != scores[i]:
            checkScoreFail(card)
        else:
            checkScorePass(card.face)
    #End checkScore

def cardTest():
    print("--Card Test--")

    newCardNotNull()
    cardToString()
    checkScore()

# Execute tests below this line.
cardTest()

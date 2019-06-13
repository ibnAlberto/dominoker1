## Domino's simulator

import random
from operator import attrgetter

class Domino(object):
    smallerNumber = 0
    largerNumber = 0
    total = 0
    isDouble = 0
    leftNumber = -1
    rightNumber = -1

    def __init__(self, side1, side2):
        self.smallerNumber = min(side1,side2)
        self.largerNumber = max(side1,side2)

        self.total = side1 + side2

        if side1 == side2: self.isDouble = 1
        else: self.isDouble = 0

	def __eq__(self, other):
		return self.smallerNumber == other.smallerNumber and self.largerNumber == other.largerNumber



class dominoHand(object):
	listOfDominos = []
	currentPointsInHand = 0
	dominosInHand = 0
	largestDouble = -1
	largestDoubleDomino = Domino(-1,-1)

	def __init__(self, inputListOfDominos):
		self.listOfDominos = inputListOfDominos

		self.dominosInHand = len(self.listOfDominos)

		for dominoInHand in self.listOfDominos:
			self.currentPointsInHand += dominoInHand.smallerNumber + dominoInHand.largerNumber

			if dominoInHand.isDouble and dominoInHand.smallerNumber > self.largestDouble:
				self.largestDouble = dominoInHand.smallerNumber
				self.largestDoubleDomino = dominoInHand

	def findLargestDouble(self):
		ordered_dominoHand = sorted(self.listOfDominos, key=lambda x: x.total, reverse=True)
		for specificDomino in ordered_dominoHand:
			if specificDomino.isDouble: return [specificDomino.smallerNumber, specificDomino]
		return [-1, Domino(-1,-1)]


	def removeDomino(self, specificDomino):
		self.listOfDominos.remove(specificDomino)
		self.dominosInHand -= 1
		self.currentPointsInHand -= specificDomino.total

		########
		#	update largest double information
		#
		#	may be useful for certain domino choosing techniques
		########
		if specificDomino == self.largestDoubleDomino:
			[self.largestDouble , self.largestDoubleDomino] = self.findLargestDouble()

	def printHand(self, supress=False):
		if self.dominosInHand: 
			desiredList = [ (x.smallerNumber,x.largerNumber) for x in self.listOfDominos]
		else: desiredList = ['empty hand']
		if supress: return desiredList
		print desiredList


#
# input (game state machine, hand to play) 
#	|
#	\/
# game state machine
#	|
#	\/
# output (game state machine)
# 

class gameSM(object):
	listOfDominosOnTable = []
	count = 0


	def __init__(self, orderedListOfHands):
		self.orderedListOfHands = orderedListOfHands

#	def playFromHand():
#		pass

#	def playLargestDouble():
#		pass

	# def playSmallestFromHand():
	# 	pass

	# def playLeftestFromHand():
	# 	pass

	def printDominosOnTable(self,listOfDominosOnTable, supress=False):
		desiredList = [(x.leftNumber,x.rightNumber) for x in listOfDominosOnTable]
		if supress: return desiredList
		print desiredList


	def checkLeft(self, specificDomino,listOfDominosOnTable):
		if not len(listOfDominosOnTable): return True
		return listOfDominosOnTable[0].leftNumber in [specificDomino.smallerNumber,specificDomino.largerNumber]

	def checkRight(self, specificDomino,listOfDominosOnTable):
		if not len(listOfDominosOnTable): return True
		return listOfDominosOnTable[-1].rightNumber in [specificDomino.smallerNumber,specificDomino.largerNumber]

	def checkDomino(self, specificDomino,listOfDominosOnTable):
		return self.checkLeft(specificDomino,listOfDominosOnTable) or self.checkRight(specificDomino,listOfDominosOnTable)

	def pickDirection(self,specificDomino,listOfDominosOnTable):
		if (not self.checkLeft(specificDomino,listOfDominosOnTable)) or (self.checkLeft(specificDomino,listOfDominosOnTable) and self.checkRight(specificDomino,listOfDominosOnTable) and random.choice([True, False])):
			return 'Right'
		else: return 'Left'

	def appendDomino(self,specificDomino,listOfDominosOnTable, direction):
		###
		### update leftNumber/rightNumber for specificDomino
		###

		if not len(listOfDominosOnTable):
			specificDomino.leftNumber=specificDomino.smallerNumber
			specificDomino.rightNumber=specificDomino.largerNumber
			return [specificDomino]

		if direction == 'Right':
			matchingIndex = [specificDomino.smallerNumber,specificDomino.largerNumber].index(listOfDominosOnTable[-1].rightNumber)
			### matchingIndex becomes leftNumber of newly added Domino
			specificDomino.leftNumber = [specificDomino.smallerNumber,specificDomino.largerNumber][matchingIndex]
			specificDomino.rightNumber = [specificDomino.smallerNumber,specificDomino.largerNumber][matchingIndex-1]
			listOfDominosOnTable.append(specificDomino)
		else:
			matchingIndex = [specificDomino.smallerNumber,specificDomino.largerNumber].index(listOfDominosOnTable[0].leftNumber)
			### matchingIndex becomes rightNumber of newly added Domino
			specificDomino.rightNumber = [specificDomino.smallerNumber,specificDomino.largerNumber][matchingIndex]
			specificDomino.leftNumber = [specificDomino.smallerNumber,specificDomino.largerNumber][matchingIndex-1]
			listOfDominosOnTable.insert(0,specificDomino)

		return listOfDominosOnTable

	def playDomino(self, specificDomino, direction, orderedListOf_dominoHand, lastFourMoves, listOfDominosOnTable):

		newListOfDominosOnTable = self.appendDomino(specificDomino,listOfDominosOnTable, direction)


		###
		### Most recent play is at the front of lastFourMoves
		###


		if len(lastFourMoves) == 4:
			newLastFourMoves = ['play']+ lastFourMoves[:-1]
		else:
			lastFourMoves.insert(0,'play')
			newLastFourMoves = lastFourMoves

#		print "before", orderedListOf_dominoHand[0].dominosInHand
#		print specificDomino.smallerNumber, specificDomino.largerNumber
		orderedListOf_dominoHand[0].removeDomino(specificDomino)
#		print [(x.smallerNumber, x.largerNumber) for x in orderedListOf_dominoHand[0].listOfDominos]
#		print "after", orderedListOf_dominoHand[0].dominosInHand
		newOrderedListOf_dominoHand = orderedListOf_dominoHand[1:] + orderedListOf_dominoHand[:1]

		return [newOrderedListOf_dominoHand, newLastFourMoves, newListOfDominosOnTable]


#######
#######
#######	Flesh Out "play largest Double" for first play of the game [playLargestFromHand is ok approx]
#######		move playChoices (playRandom, playLargest, playSmallest) in "Domino Hand Class"
#######		
#######
#######

	def playLargestFromHand(self,orderedListOf_dominoHand, lastFourMoves, listOfDominosOnTable):

		#iterate through dominos ordered by size, checking if they work (new list)
		ordered_dominoHand = sorted(orderedListOf_dominoHand[0].listOfDominos, key=lambda x: x.total, reverse=True)

		#print [(x.smallerNumber, x.largerNumber) for x in ordered_dominoHand]

		####
		#### Sauce 1. WHICH DOMINO TO PLAY
		####

		for specificDomino in ordered_dominoHand:
			if self.checkDomino(specificDomino, listOfDominosOnTable):

				###
				###	Sauce 2. WHICH DIRECTION TO PLAY IN CASE OF CAPICUA
				###

				direction = self.pickDirection(specificDomino, listOfDominosOnTable)

				return self.playDomino(specificDomino, direction, orderedListOf_dominoHand, lastFourMoves, listOfDominosOnTable)


		# or Pass

		# print "we are passing here", orderedListOf_dominoHand[0].printHand(1)
		# print "ordered_dominoHand", dominoHand(ordered_dominoHand).printHand(1)
		# self.printDominosOnTable(listOfDominosOnTable)


		###
		### Most recent play is at the front of lastFourMoves
		###


		newOrderedListOf_dominoHand = orderedListOf_dominoHand[1:] + orderedListOf_dominoHand[:1]
		if len(lastFourMoves) == 4:
			newLastFourMoves = ['pass']+ lastFourMoves[:-1]
		else:
			lastFourMoves.insert(0,'pass')
			newLastFourMoves = lastFourMoves
		newListOfDominosOnTable = listOfDominosOnTable

		return [newOrderedListOf_dominoHand, newLastFourMoves, newListOfDominosOnTable]

#
# input (game state machine, hand to play) 
#	|
#	\/
# game state machine
#	|
#	\/
# output (game state machine)
# 


	def playGame(self, orderedListOf_dominoHand, lastFourMoves, listOfDominosOnTable):
		self.count += 1
		# print "count", self.count
		# print "lastFourMoves", lastFourMoves
		if (lastFourMoves.count('pass')<4) and orderedListOf_dominoHand[-1].dominosInHand and self.count<200:
			[newOrderedListOf_dominoHand, newLastFourMoves, newListOfDominosOnTable] = self.playLargestFromHand(orderedListOf_dominoHand, lastFourMoves, listOfDominosOnTable)
			self.playGame(newOrderedListOf_dominoHand, newLastFourMoves, newListOfDominosOnTable)
		else:
			print "final table:", self.printDominosOnTable(listOfDominosOnTable,1)
			print "hands:"
			for idx, x in enumerate(orderedListOf_dominoHand):
				print 'Hand', str(idx+1), str(x.printHand(1))
				print 'Total Points', x.currentPointsInHand
			print "yay we won!"

listOfAllDominos = []

for side1 in range(10):
	for side2 in range(side1,10):
		listOfAllDominos.append(Domino(side1,side2))

def generateFourHands(listOfDominos):
	selectedFortyOnTheTable = random.sample(listOfDominos, 40)
	hand1 = dominoHand(selectedFortyOnTheTable[:10])
	hand2 = dominoHand(selectedFortyOnTheTable[10:20])
	hand3 = dominoHand(selectedFortyOnTheTable[20:30])
	hand4 = dominoHand(selectedFortyOnTheTable[30:])
	return [hand1,hand2,hand3,hand4]

fourHands = generateFourHands(listOfAllDominos)

firstPlayer = max(fourHands, key=attrgetter('largestDouble'))

desiredIndex = fourHands.index(firstPlayer)
# print desiredIndex, firstPlayer.largestDouble

reorderdFourHands = fourHands[desiredIndex:] + fourHands[:desiredIndex]




#######
#######
#######	Main Game Code
#######
#######

initGame = gameSM(reorderdFourHands)

initGame.playGame(reorderdFourHands,[],[])

#######
#######
#######	Flesh Out Iterative testing, how many times "1 point" or "tie" or "straight connected" or "doubles traveling together"
#######		which combination of play styles 
#######			yield highest winning percentages
#######
#######		how often does second player pass?
#######
#######


#######
#######
#######	Develop Probabalistic Model for player to guess what other players have played, when they passed, what is on the table
#######
#######


# first domino is placed, smaller on Left, Larger on Right
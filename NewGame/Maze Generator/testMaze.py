from maze import *
import playerMaze
import genmaze

import random
import sys
import copy

def printResult(text, numPassed, totalTests, truth):
	'''Formats the print result.'''
	text = text + (30 - len(text)) * ' '

	if truth:
		print(text + "PASSED {} / {}".format(numPassed, totalTests))
	else:
		print(text + "FAILED {} / {}".format(numPassed, totalTests))


def test(numRows, numCols, numPlayers, threshold, verbose = False):
	numPassed = 0
	totalTests = 2 + numPlayers

	if numRows == 10 and numCols == 15 and numPlayers == 2:
		totalTests += 18

	testMaze = genmaze.main(numRows, numCols, numPlayers, threshold,\
	 verbose, True)

	# We first checked that all the cells have been visited
	visitedPassed = True
	for row, col in ((r, c) for r in range(testMaze.numRows) \
							for c in range(testMaze.numColumns)):
		if not testMaze.isVisited(row, col):
			visitedPassed = False
			break
	if visitedPassed:
		numPassed += 1
	printResult("ALL GEN CELLS VISITED", numPassed, totalTests, visitedPassed)

	
	# We also check that the player start locations have been added
	passed = (len(testMaze.start) > 0)
	if passed:
		numPassed += 1
	printResult("PLAYER START LOC ON MAZE", numPassed, totalTests, passed)

	# We check that the player location is logged in their own classes
	players = []
	for play in range(numPlayers):
		players.append(playerMaze.playerMaze(testMaze, testMaze.start[play]))

		passed = (players[play].getCurrentLocation() == testMaze.start[play])

		if passed:
			numPassed += 1
		printResult("PLAYER START LOC SAVED", numPassed, totalTests, passed)
		
	# Using the test case of 10 rows and 15 cols with seed 'TestSeed'
	# with 2 players
	if numRows == 10 and numCols == 15 and numPlayers == 2:
		p1 = players[0]
		p2 = players[1]

	else:
		return numPassed

	# Test player 1 can move North and West but not East and South.
	passed = p1.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK NORTH", numPassed, totalTests, passed)

	passed = not p1.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK EAST", numPassed, totalTests, passed)

	passed = not p1.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK SOUTH", numPassed, totalTests, passed)

	passed = p1.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK WEST", numPassed, totalTests, passed)

	# Then attempt a move North. Check can only move South.
	p1.moveLocation("North")
	passed = (p1.getCurrentLocation() == (0, 14))
	if passed:
		numPassed += 1
	printResult("* PLAYER ONE MOVE NORTH *", numPassed, totalTests, passed)

	passed = not p1.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK NORTH", numPassed, totalTests, passed)

	passed = not p1.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK EAST", numPassed, totalTests, passed)

	passed = p1.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK SOUTH", numPassed, totalTests, passed)

	passed = not p1.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK WEST", numPassed, totalTests, passed)

	# Test player 2 can move West but not North, East, or South.
	passed = not p2.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK NORTH", numPassed, totalTests, passed)

	passed = not p2.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK EAST", numPassed, totalTests, passed)

	passed = not p2.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK SOUTH", numPassed, totalTests, passed)

	passed = p2.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER TWO CHECK WEST", numPassed, totalTests, passed)

	# Then attempt a move West. Check can move East or South
	p2.moveLocation("West")
	passed = (p2.getCurrentLocation() == (5, 13))
	if passed:
		numPassed += 1
	printResult("* PLAYER ONE MOVE NORTH *", numPassed, totalTests, passed)

	passed = not p2.checkMove("North")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK NORTH", numPassed, totalTests, passed)

	passed = p2.checkMove("East")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK EAST", numPassed, totalTests, passed)

	passed = p2.checkMove("South")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK SOUTH", numPassed, totalTests, passed)

	passed = not p2.checkMove("West")
	if passed:
		numPassed += 1
	printResult("PLAYER ONE CHECK WEST", numPassed, totalTests, passed)

	moves = ["South", "West", "South", "South", "West", "South", "East", \
				"East", "North", "North", "South", "South", "West", "West", \
				"South", "South", "West", "North", "West", "West", "West", \
				"South", "West", "West", "West", "West", "North", "North"]
	for move in moves:
		if p1.checkMove(move):
			p1.moveLocation(move)
		else:
			break

	p1.print()
	p2.print()

if __name__ == '__main__':
	numRows = 10
	numCols = 15
	if len(sys.argv) > 1:
		numRows = int(sys.argv[1])
		numCols = int(sys.argv[2])

	if len(sys.argv) > 3:
		numPlayers = int(sys.argv[3])
	else:
		numPlayers = 2

	if len(sys.argv) > 4:
		threshold = int(sys.argv[4])
	else:
		threshold = 10

	random.seed('TestSeed')
	test(numRows, numCols, numPlayers, threshold)
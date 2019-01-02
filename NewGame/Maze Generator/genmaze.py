from maze import *
import random
import sys
import copy

def addDirectionOption(Maze, row, column, direction, dir_list):
	''' Adds a direction to the list of possible directions'''
	(neighbor_row, neighbor_col) = Maze.getNeighborCell(row, column, direction)

	if not Maze.isVisited(neighbor_row, neighbor_col):
		dir_list.append(direction)

def numWalls(Maze, cellRow, cellCol):
	''' Check has number of walls'''
	wall_num = 0

	if Maze.hasWall(cellRow, cellCol, "North"):
		wall_num += 1
	if Maze.hasWall(cellRow, cellCol, "East"):
		wall_num += 1
	if Maze.hasWall(cellRow, cellCol, "South"):
		wall_num += 1
	if Maze.hasWall(cellRow, cellCol, "West"):
		wall_num += 1

	return wall_num

def findFurthestSharedCell(Maze, numShare):
	'''We want to find the furthest cell from the exit that appears more than
	once. '''
	# We first want to sort the list to put the higher numbers (cells further
	# from the exit) at the front of the list
	cellNumList = sorted(Maze.cellNumToExit)[::-1]

	for cell in cellNumList:
		# If the cell is repeated, then we found our candidate
		if cellNumList.count(cell) >= numShare:
			return cell 
	# If there is no candidate, then there is only one path in the entire
	# maze. Notify the calling function.
	return -1

def findNumDirectionOptions(Maze, row, col):
	'''Given a cell on the maze (described by a (row, col) coordinate), return
	the number of options (North, South, East, West) that can be explored. '''
	options = []
			
	# Check that there is room to the NORTH
	if row > 0:
		addDirectionOption(Maze, row, col, "North", options)

	# Also check that there is room to the SOUTH
	if row < Maze.numRows - 1:
		addDirectionOption(Maze, row, col, "South", options)

	# Also check that there is room to the WEST
	if col > 0:
		addDirectionOption(Maze, row, col, "West", options)

	# Lastly, check that there is room to the EAST
	if col < Maze.numColumns - 1:
		addDirectionOption(Maze, row, col, "East", options)

	# Now options should only a max of 4 options. These will exclude
	# walls and locations that have already been visited.
	assert(len(options) <= 4)
	assert(len(options) >= 0)

	return options


def findAllIndices(inList, val):
	'''Return a list of all the indices which contain the given value 'val' '''
	indexList = []

	for index, item in enumerate(inList):
		if item == val:
			indexList.append(index)

	return indexList

def findNewHead(Maze, inList, verbose = False):
	'''Takes in a list of the form [(row, col), ...] and finds the first list
	wear the numOptions is greater than zero.'''
	if inList == [] and verbose:
		print("EMPTY LIST AS INPUT")

	for index, coord in enumerate(inList):
		r, c = coord
		numOptions = len(findNumDirectionOptions(Maze, r, c))
		if numOptions > 0:
			# We have found a new head
			if verbose:
				print("NEW HEAD FOUND \t", coord, " with ",\
							numOptions, " option(s)")
			return inList[:index + 1]
	# if there is no new head...
	if verbose:
		print("NO HEAD")

	return []

def findNewPath(Maze, availList, verbose = False):
	'''Given the state of the maze and explored paths. It finds a new path if
	possible.'''
	# In the new generator, we want to restart at the end and find
	# the earliest location that had options.
	# print("FINDING NEW PATH")
	
	availList.sort(key = lambda x : len(x))

	# print("Num Paths:" , len(availList))
	iterList = copy.deepcopy(availList)

	for possPath in iterList:
		oldPath = copy.deepcopy(possPath)
		newPath = findNewHead(Maze, possPath, verbose)	

		if newPath != []:
			availList.append(newPath)
			return newPath

		# If the path has not changed (gone through all possibilites),
		# then the path is dry, can be removed and we need to consider
		# a new path.
		else:
			availList.remove(oldPath)

	return []



def genMaze(numRows, numCols, threshold, verbose = False):
	''' This function generates the maze'''
	m = Maze(numRows, numCols)
	m.clear()
	m.setAllWalls()
	m.setVisited(m.end[0], m.end[1])

	path = []
	availPaths = []
	availPaths.append(path)

	path.append(m.end)

	while not len(path) == 0:
		if (verbose):
			print("Num Paths:" , len(availPaths))

		# Add current location to the path
		(current_r, current_c) = path[len(path) - 1]

		# This list will contain the direction options to expand the 
		# maze from the current Location.
		# IMPORTANT: We want options to reset after every loop
		options = findNumDirectionOptions(m, current_r, current_c)

		# If options is empty (i.e. surrounded by visited/walls):
		# There are no directions we can move from the current cell! We
		# need to backtrack.
		# Note: option size cannot be negative.
		if len(options) == 0:
			# In the new generator, we want to restart at the end and find
			# the earliest location that had options.
			if verbose:
				print("FIXING DEAD END")
			# path.pop()
			path = findNewPath(m, availPaths, verbose)

		# Now we can continue the loop.
		else:
			# Choose a random direction! Then, clear the wall in that 
			# direction, and move into the next cell.
			dir_rand = random.choice(options)

			# Now, clear the wall in that direction and 
			# move into the next cell.
			m.clearWall(current_r, current_c, dir_rand)
			(next_row, next_col) = m.getNeighborCell(current_r, \
													 current_c, \
													 dir_rand)

			# Mark the cell at next location as VISITED. 
			# Note that START is already marked as VISITED.
			m.setVisited(next_row, next_col)
			m.setCellNum(next_row, next_col, len(path))

			# Append next location onto the path.
			availPaths.remove(path)
			path.append((next_row, next_col))
			availPaths.append(path)


			# If our path is now longer than the threshold, we need to 
			# increase the threshold to allow exploration of the entire map.
			if len(path) >= threshold:
				if (verbose):
					print("ADJUSTING THRESHOLD")
				threshold += 1

				# We want to switch to a shorter path.
				availPaths.sort(key = lambda x : len(x))
				path = findNewPath(m, availPaths, verbose)

	if verbose:
		print("Ending Number of paths:", len(availPaths))
	# Return the competed maze
	return m
		
		

def main(numRows, numCols, numPlayers, threshold, coinPercent, verbose = False,\
			printMaze = True):
	'''Wraps together all maze generation functions. '''

	# We first want to generate the maze
	m = genMaze(numRows, numCols, threshold, verbose)

	if verbose:
		m.print()
	testlist = sorted(m.cellNumToExit, reverse = True)

	if verbose:
		print("Sorted List:", testlist[:15])
		print(findFurthestSharedCell(m, numPlayers))

	# Now we want to designate the start values given the results of the
	# two shared locations that are furthest away.
	furthestSharedNum = findFurthestSharedCell(m, numPlayers)
	sharedCells = findAllIndices(m.cellNumToExit, furthestSharedNum)

	for player in range(numPlayers):
		playerCell = m.getCoordFromIndex(sharedCells[player])
		m.start.append(playerCell)

		if printMaze:
			print("Player {} starts at {}".format(player + 1,playerCell))

	m.setCoin(coinPercent)

	if printMaze:
		m.print(verbose = False)

	return m


def usage(name):
	''' Show usage imformation for our program'''
	print("usage:", name, "n f p t")
	print("n is an integer of total maze rows")
	print("f is an integer of total maze columns")
	print("p is an integer of number of players")
	print("t is an integer of threshold length in maze generation")


if __name__ == '__main__':

	if len(sys.argv) < 3:
		print("Too Few Arguments!")
		usage(sys.argv[0])
	else:
		if len(sys.argv) >= 3:
			numRows = int(sys.argv[1])
			numCols = int(sys.argv[2])

		if len(sys.argv) > 3:
			numPlayers = int(sys.argv[3])
		else:
			numPlayers = 2

		if len(sys.argv) > 4:
			coinPercent = float(sys.argv[4])	
		else:
			coinPercent = 0.05

		if len(sys.argv) > 5:
			threshold = int(sys.argv[5])
		else:
			threshold = 10
 
		main(numRows, numCols, numPlayers, threshold, coinPercent, False)

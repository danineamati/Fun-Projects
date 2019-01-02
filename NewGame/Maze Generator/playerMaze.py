from maze import *
import random
import sys

class playerMaze():
	"""Stores the maze, player location, and what the player can view."""
	def __init__(self, maze, startLoc):
		self.maze = maze
		self.currLoc = startLoc # in the form (row, col)
		self.visited = [startLoc] # Stores visited locations
		self.canViewEnd = self.checkViewEnd()

	def savePlayerMaze(self, fileName):
		pass

	def loadPlayerMaze(self, fileName):
		pass

	def getCurrentLocation(self):
		'''Returns current location.'''
		return self.currLoc

	def addNewLocation(self, loc):
		'''Sets new location for the player and adds it to the list of visited
		locations.'''
		self.visited.append(loc)
		self.currLoc = loc
		self.canViewEnd = self.checkViewEnd()

	def moveLocation(self, direction):
		'''Moves to new location given ['North', 'East', 'South', 'West'] 

		The Direction list is specified in maze.py'''
		current_row, current_col = self.currLoc
		assert(not self.maze.hasWall(current_row, current_col, direction))
		new_row, new_col = self.maze.getNeighborCell(\
			current_row, current_col, direction)
		self.addNewLocation((new_row, new_col))

	def checkMove(self, direction):
		'''Checks if player can move in given direction.'''
		current_row, current_col = self.currLoc
		return not self.maze.hasWall(current_row, current_col, direction)

	def checkViewEnd(self):
		'''Checks if the player can see or has seen the end. '''
		# Check the adjacent locations to the end.
		for direction in Direction:
			adjacent = self.maze.getNeighborCell(self.maze.end[0], \
								self.maze.end[1], direction)
			# if the adjacent cell is the current location
			# AND there is not wall in the way,
			if adjacent == self.currLoc and \
					not self.maze.hasWall(adjacent[0], adjacent[1], direction):
				return True
		# Otherwise, 
		return False

	def print(self):
		'''Outputs the maze using simple ASCII-art to the specified output.
		The output format is as follows, using the example maze from the
		assignment write-up.  (The text to the right of the maze is purely
		explanatory, and you don't need to output it.)
		
		3 4               (# of rows and then # of columns)
		+---+---+---+---+ (each cell is 3 spaces wide, with a + at each corner)
		| -   - | X   X |   (walls indicated by --- or |)
		+---+   +   +   +   (Player Location indicated by P)
		| X | - | X | X |   (Visited indicated by V)
		+   +   +   +   +
		|     P     | X |
		+---+---+---+---+
		 '''

		print()
		print(self.maze.numRows, self.maze.numColumns)

		top_wall = '+'
		for c in range(self.maze.numColumns):
			if (0, c) in self.visited and self.maze.hasWall(0, c, "North"):
					top_wall += '---+'
			else:
				top_wall += '   +'
		print(top_wall)

		def print_cell(content, r, c):
			'''Prints the cell and the wall for a given content'''
			current = content
			if (r, c) in self.visited and self.maze.hasWall(r, c, "East"):
				current += '|'
			elif c < self.maze.numColumns - 1 and \
						(r, c + 1) in self.visited and \
						self.maze.hasWall(r, c + 1, "West")	:
				current += '|'
			else:
				current += ' '
			return current
		
		for r in range(self.maze.numRows):
			current_row = ''

			if (r, 0) in self.visited and self.maze.hasWall(r, 0, "West"):
				current_row += '|'
			# if c > 0 and (r, c - 1) in self.visited and \
			# 	self.maze.hasWall(r, c - 1, "East")	:
			# 	current_row += '|'
			else:
				current_row += ' '
			
			for c in range(self.maze.numColumns):
				if (r, c) == self.getCurrentLocation():
					current_row += print_cell(' P ', r, c)

				elif (r, c) in self.visited:
					current_row += print_cell(' - ', r, c)

				elif self.canViewEnd and (r, c) == self.maze.end:
					current_row += print_cell(' E ', r, c)

				else:
					current_row += print_cell('   ', r, c)

			print(current_row)

			current_floor = '+'
			if r < self.maze.numRows:
				for c in range(self.maze.numColumns):
					if (r, c) in self.visited and \
										self.maze.hasWall(r, c, "South"):
						current_floor += '---+'
					elif r < self.maze.numColumns and \
										(r + 1, c) in self.visited and \
										self.maze.hasWall(r + 1, c, "North")	:
						current_floor += '---+'
					else:
						current_floor += '   +'
				print(current_floor)
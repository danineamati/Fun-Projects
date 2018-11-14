import pygame

white = (255,255,255)
grey = (128,128,128)
black = (0,0,0)

class mapHandler():
	"""Handles the display and covering of parts of the map."""
	def __init__(self, mapImage, compassImage,
				width = 640, height = 640, caption = 'D&D Map'):
		pygame.init()
		self.width = width
		self.height = height
		self.caption = caption

		self.mapImage = pygame.image.load(mapImage)
		self.compassImage = pygame.image.load(compassImage)

		# Initialize for later in format (x1, y1), (x2, y2)
		self.mapLoc = ((0,0),(0,0))

		# To preserve image ratio
		self.ratio = self.mapImage.get_width() / self.mapImage.get_height()

		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('D&D Map')

		Background = pygame.Surface(self.window.get_size())
		self.Background = Background.convert()
		self.Background.fill((0,0,0))
		self.backRect = pygame.Rect(self.getBackRectDimensions())

		# Put the map and the compass
		self.setMapImage()
		self.updateBackgroundLoc()
		self.compass()

		self.clock = pygame.time.Clock()

		self.rectLists = []

	def getBackRectDimensions(self):
		'''Gets the dimensions such that the rectangle is at the center
		of the screen.'''

		# Get the center of the window
		xMid = self.width / 2
		yMid = self.height / 2

		# If the image ratio is greater than 1, the width is larger than
		# the height. Set the width to be the same as the width of the window
		x1, y1 = 0, 0

		if self.ratio >= 1:
			x2 = self.width 
			y2 = self.width / self.ratio

			# Map Loc in format (x1, y1), (x2, y2)
			self.mapLoc = ((0, yMid - (xMid / self.ratio)), 
				(self.width, yMid + (xMid / self.ratio)))
		else:
			# Else, repeat but with the height maximized
			x2 = self.height * self.ratio
			y2 = self.height 

			# Map Loc in format (x1, y1), (x2, y2)
			self.mapLoc = ((xMid - (yMid * self.ratio), 0), 
				(xMid + (yMid * self.ratio), self.height))

		return (x1, y1), (x2, y2)

	def setMapImage(self):
		'''Makes a surface that maximizs the map image to the screen.'''
		self.mapImage = pygame.transform.scale(self.mapImage, 
												self.backRect.size)
		self.mapImage = self.mapImage.convert()

		self.Background.blit(self.mapImage, self.backRect)

	def updateBackgroundLoc(self, center = True):
		'''Puts the Background map centered with the screen.'''
		x = self.width / 2
		y = self.height / 2
		width = self.backRect.x
		height = self.backRect.y

		if center:
			print(self.mapLoc)
			self.window.blit(self.Background, self.mapLoc[0])
		else:
			self.window.blit(self.Background, (0,0))

	def compass(self):
		'''Puts the compass at the top left'''
		self.compassImage = pygame.transform.scale(self.compassImage, 
												(150, 150))
		self.window.blit(self.compassImage, (0,0))

	def drawRect(self, topLeft, bottomRight):
		'''Draws a rectangle by defining the top left and bottom right 
		corners.'''
		# First determine the actual top left
		if topLeft[0] > bottomRight[0]:
			topLeft, bottomRight = bottomRight, topLeft

		width = abs(topLeft[0] - bottomRight[0])
		height = abs(topLeft[1] - bottomRight[1])
		rect1 = pygame.draw.rect(self.window, black, 
	            	 		(topLeft[0], topLeft[1],
	            	 		width, height))

		self.rectLists.append(rect1)
		print(rect1.x, rect1.y)

	def redrawAll(self):
		'''Redraws necessary screen contents such as map, compass, 
		and rectangles'''
		self.updateBackgroundLoc()
		
		for rectKept in self.rectLists:
			pygame.draw.rect(self.window, black, 
	            	 		(rectKept.x, rectKept.y, 
	            	 			rectKept.width, rectKept.height))
		self.compass()

	def inBox(self, pos):
		'''Returns the first index that the coordinate (x, y) is in.'''
		x, y = pos
		for num, myRect in enumerate(self.rectLists):
			if (x > myRect.x) and (x < myRect.x + myRect.width) and \
				(y > myRect.y) and (y < myRect.y + myRect.height):
				print("in box")
				return num

	def removeBox(self, pos):
		'''Removes box from visible screen.'''
		try:
			num = self.inBox(pos)
			self.rectLists.pop(num)
		except TypeError as e:
			print(e)

	def gameLoop(self):
	    end = False

	    rectSet = False
	    topLeft = (0, 0)

	    while not end:
	        for event in pygame.event.get():
	            if event.type == pygame.QUIT:
	            	end = True
	            	pygame.quit()
	            	quit()
	            if event.type == pygame.KEYDOWN:
	                if event.key == pygame.K_q:
	                    end = True
	                    pygame.quit()
	                    quit()
	                if event.key == pygame.K_r:
	                	pygame.draw.rect(self.window,
	                		black,(300,150,200,50))
	                if event.key == pygame.K_c:
	                	self.updateBackgroundLoc()
	                	self.compass()
	                if event.key == pygame.K_u:
	                	self.redrawAll()
	                if event.key == pygame.K_d:
	                	pos = pygame.mouse.get_pos()
	                	print(pos)
	                	self.removeBox(pos)
	                	self.redrawAll() 

	            if event.type == pygame.MOUSEBUTTONDOWN:
	            	pos = pygame.mouse.get_pos()
	            	print(pos)
	            	if rectSet:
	            		self.drawRect(topLeft, pos)
	            		rectSet = False
	            		self.compass()
	            	else:
	            		topLeft = pos
	            		rectSet = True

	        pygame.display.update()
	        self.clock.tick(60)


if __name__ == '__main__':
	myMap = mapHandler('Maps\\TestMap4.png', 'Maps\\compass-rose-color.png')
	myMap.gameLoop()



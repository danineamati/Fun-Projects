import pygame
pygame.init()

windowRatio = 2 / 3

windowW = 1000
windowL = int(windowW * windowRatio)

window = pygame.display.set_mode((windowW, windowL))
pygame.display.set_caption('Pokemon party')

clock = pygame.time.Clock()

white = (255,255,255)
grey = (128,128,128)
black = (0,0,0)

margin = 50
inner_margin = margin

imageHeight = int((windowL - 3 * inner_margin - 2 * margin) / 2)
imageWidth = int((windowW - 4 * inner_margin - 2 * margin) / 3)

# Calculate the upper left corner of each image
# upper and lower
# left, middle, and right
upper = margin + inner_margin
lower = margin + 2 * inner_margin + imageHeight

left = margin + inner_margin
middle = margin + 2 * inner_margin + imageWidth
right = margin + 3 * inner_margin + 2 * imageWidth

def placeholderRects():
	ul = pygame.draw.rect(window, white, \
						 [left, upper, imageWidth, imageHeight])
	ll = pygame.draw.rect(window, white, \
						 [left, lower, imageWidth, imageHeight])
	um = pygame.draw.rect(window, white, \
						 [middle, upper, imageWidth, imageHeight])
	lm = pygame.draw.rect(window, white, \
						 [middle, lower, imageWidth, imageHeight])
	ur = pygame.draw.rect(window, white, \
						 [right, upper, imageWidth, imageHeight])
	lr = pygame.draw.rect(window, white, \
						 [right, lower, imageWidth, imageHeight])

def pictureSetUp(filename, corner):
	pic = pygame.image.load(filename)
	pic = pygame.transform.scale(pic, (imageWidth, imageHeight))
	picRect = pic.get_rect()
	picRect = picRect.move(corner)
	window.blit(pic, picRect)
	return pic

def gameLoop():
	end = False
	while not end:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		window.fill(black)

		pygame.draw.rect(window, (50,50,50), [margin, margin, \
			windowW - margin * 2,windowL - margin * 2])

		swampert = pictureSetUp("Pokemon_Images\\260Swampert.png", \
														(left, upper))
		latios = pictureSetUp("Pokemon_Images\\381Latios.png", \
														(middle, upper))
		#Causing an error to display
		luxray = pictureSetUp("Pokemon_Images\\405Luxray.png", \
														(right, upper))
		castform = pictureSetUp("Pokemon_Images\\351Castform.png", \
														(left, lower))
		chandelure = pictureSetUp("Pokemon_Images\\609Chandelure.png", \
														(middle, lower))
		aegislash = pictureSetUp("Pokemon_Images\\681Aegislash.png", \
														(right, lower))
		#Causing an error to display

		pygame.display.update()
		clock.tick(60)

gameLoop()
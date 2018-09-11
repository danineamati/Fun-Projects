from tkinter import *
from tkinter import font
import random
import math

def drawCircle(x, y, r, color, canvas):
    ''' This function will draw a circle on the canvas. The center is at x, y
    and the r is the radius. There is also a color argument the determines the
    color of the circle.
    The function returns the handle of the circle object.'''
    circle = canvas.create_oval(x - r, y - r, x + r, y + r,\
                                fill = color, outline = color)
    #circles.append(circle)
    return circle

def randomCircles(x, y, rMax, planet, back_color, canvas):
    ''' This function creates random circles at random locations on the planet
    of designated color'''
    vege_color = {
            'Carnivorus Plants' : 'medium aquamarine',
            'Tentacles' : 'indian red',
            'Metal Trees' : '#979A9A',
            'Organic Spikes' : 'dark olive green',
            'Giant Lilypads' : 'dark sea green',
            'Trees' : 'dark green'                        
    }
    
    # Generates an integer number of circles based on planet sea level
    # 33 is completly arbitrary
    numCircles = int((1 - planet.surf_water) * 10)
    vege_specific = vege_color[planet.vege_type]

    for circle in range(numCircles):
        r_circle = random.randint(10, int(0.5 * rMax))
        # r_1 is the distance from the center of the planet to the center of
        # the randomly generated circle
        r_1 = (random.random() + 0.25) * (rMax - r_circle - (0.25 * (rMax - r_circle)))
        theta = random.random() * (2 * math.pi)
        delta_x = r_1 * math.cos(theta)
        delta_y = -r_1 * math.sin(theta)
        circ_color = back_color
        if (random.random() * planet.vege_amt) < (planet.vege_amt * planet.vege_amt):
            circ_color = vege_specific
            
        circ_handle = drawCircle(x + delta_x, y + delta_y, r_circle,\
                                 circ_color, canvas)
        #circles.append(circ_handle)

class Planets:
    ''' This class generates a planet based on random factors.'''
    def __init__(self, name, canvas):
        ''' Creates a planet from randomly determined features.'''
        self.name = name
        self.canvas = canvas
        self.radius = random.randint(50, 250)
        
        self.day = random.random() * 30
        if self.day == 0: # Ensure day + night > 0
            self.night = (random.random() + 0.1) * 30
        else:
            self.night = random.random() * 30
        self.daynight = self.day + self.night
        
        self.surf_water = random.random() # Percentage of water
        # 0 == NO WATER!!! and 1 == NO LAND!!!
        
        self.vege_amt = self.surf_water * random.random()
        # vege_amt = % of land covered by vegetation
        self.vege_type = random.choice(['Carnivorus Plants',\
                                        'Tentacles','Metal Trees',\
                                        'Organic Spikes','Giant Lilypads',\
                                        'Trees'])
        self.urban = random.random()
        # 0 = NO CITIES, 1 = CORUSCANT
        ages = ['Stone Age',\
                'Iron Age',\
                'Industrial Age',\
                'Automation Age',\
                'Artificial Age',\
                'Type 1 Civilization']
        self.tech = random.choice(ages[:int(self.urban * 6) + 1])

    def __str__(self):
        '''Return a string representing the planet.'''
        Planet_str = '''
                        Name: {}
                        Radius: {} km
                        Day: {} Earth Hours
                        Night: {} Earth Hours
                        Sol: {} Earth Hours (Total)
                        Surface Water Amount: {}% water
                        Vegetation Amount: {}% vegetated
                        Vegetation Type: {}
                        Urbanization: {}% of land urbanized
                        Technology: {}
                        '''.format(self.name, self.radius * 70,\
                                   '%.2f' % self.day,\
                                   '%.2f' % self.night,\
                                   '%.2f' % self.daynight,\
                                   '%.2f' % (self.surf_water * 100),\
                                   '%.2f' % (self.vege_amt * 100),\
                                   self.vege_type,\
                                   '%.2f' % (self.urban * 100),\
                                   self.tech)
        return Planet_str
    
    def drawPlanet(self, x, y, planet):
        '''This function draws the planet including the background, land/water,
        vegetation, clouds, etc.'''
        Land_color = '#4E342E'
        Water_color = 'RoyalBlue3'
        
        if self.surf_water < 0.5:
            back_color = Land_color
            obj_color = Water_color
        else:
            back_color = Water_color
            obj_color = Land_color

        # Now we can draw the out part of the planet
        drawCircle(x, y, planet.radius, back_color, self.canvas)

        # Now we draw the random features atop the planet surface
        randomCircles(x, y, planet.radius, planet, obj_color, self.canvas)
    
    def writePlanetSpecs(self, Planet):
        ''' This function writes the planet information to the screen. '''
        self.canvas.create_text(200, 175, text = str(Planet),\
                           fill = 'pale turquoise',\
                           font = font.Font(family = 'Copperplate Gothic Bold',\
                                            size = 11))

    def polarCaps(self, planet_x, planet_y):
        ''' This function takes a planet and generates the polar caps of the
        planet.'''
        planet_north = planet_y - self.radius
        planet_south = planet_y + self.radius

        caps_width = self.radius * 0.3

        x_ratio = 0.48
        x1 = planet_x - self.radius * x_ratio
        x2 = planet_x + self.radius * x_ratio

        caps_color = '#D6EAF8'
        # Make North Pole
        self.canvas.create_oval(x1, planet_north,\
                                x2, planet_north + caps_width,\
                                fill = caps_color, outline = caps_color)

        ratio = 1.5
        x3 = planet_x + self.radius * x_ratio / ratio
        x4 = planet_x - self.radius * x_ratio / ratio
        # Make South Pole
        self.canvas.create_oval(x3, planet_south - caps_width / 2,\
                                x4, planet_south,\
                                fill = caps_color, outline = caps_color)
        

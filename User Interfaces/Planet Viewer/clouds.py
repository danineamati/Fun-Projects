from tkinter import *
from tkinter import font
import random
import math

from planet import *
                                       
class Clouds:
    ''' This class generates the atmosphere of the planet.'''
    def __init__(self, planet, planet_x, planet_y, canvas):
        self.planet = planet
        self.planet_x = planet_x
        self.planet_y = planet_y
        self.canvas = canvas
        
        self.rect_width = planet.radius / 1.5
        self.rect_height = planet.radius / 5
        self.endcirc_radius = self.rect_height / 2
        self.color = ["#F7FAFA", "#F0F5F5", "#E8F0F0", "#E0EBEB"]
        self.max_cloud_lat = 0.75 * planet.radius
        self.min_cloud_lat = -(0.75 * planet.radius)
        
    def drawCloud(self):
        ''' Draws the clouds onscreen.'''
        delta_y = random.randrange(int(self.min_cloud_lat),\
                                   int(self.max_cloud_lat))

        inside = self.planet.radius ** 2 - delta_y ** 2
        x_para = math.sqrt(abs(inside))
        
        x = random.randrange(-(int(x_para)), int(x_para + 1)) + self.planet_x
        y = delta_y + self.planet_y

        color = random.choice(self.color)
        
        self.canvas.create_rectangle((x - self.rect_width / 2),\
                                (y - self.rect_height / 2),\
                                (x + self.rect_width / 2),\
                                (y + self.rect_height / 2), fill = color,\
                                outline = color)
        
        drawCircle(x + self.rect_width / 2, y, self.endcirc_radius,\
                        color, self.canvas)
        drawCircle(x - self.rect_width / 2, y, self.endcirc_radius,\
                        color, self.canvas)
        
    def manyClouds(self):
        ''' Draws many clouds.'''
        numClouds = self.planet.surf_water * 10
        for cloud in range(int(numClouds)):
            self.drawCloud()

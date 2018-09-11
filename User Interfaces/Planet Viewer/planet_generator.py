from tkinter import *
from tkinter import font
import random
import math

from planet import *
from clouds import *
 
if __name__ == '__main__':
    root = Tk()
    width = 1000
    height = 700
    root.geometry('{}x{}'.format(width, height))

    canvas = Canvas(root, width = width, height = height, bg = 'black')
    canvas.pack()
    
    planet_x = 750
    planet_y = 250
    
    planet1 = Planets('Vayyama', canvas)
    planet1.writePlanetSpecs(planet1)
    planet1.drawPlanet(planet_x, planet_y, planet1)
    planet1.polarCaps(planet_x, planet_y)

    cloud = Clouds(planet1, planet_x, planet_y, canvas)
    cloud.manyClouds()

    #print(font.families())
    root.bind('<q>', quit)
    root.mainloop()

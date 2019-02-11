#################################################################
# Lunar Lander 112 V1.3 - main
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## Main File: Runs the whole game, starts you off in the start menu

import pygame as pg
# pygame implemented with help from official pygame documentation page
# https://www.pygame.org/docs/
import sys

pg.init()    
    
from menuScreen import startMenu, freePlayMenu, howToPlayScreen, enterHostInfo
from classicMode import classicMode
from frenzyMode import frenzyMode
from hostServer import hostGame
from multiplayerClient import joinedGame

def main(width=1000, height=700):
    size = width, height
    pg.display.set_caption("Lunar Lander 112")
    screen = pg.display.set_mode(size)
    screenRect = screen.get_rect(topleft = (0,0))
    clock = pg.time.Clock()
    
    earthImage = pg.image.load("darkEarth.png")
    """" Image Source: 
    https://www.deviantart.com/ulimann644/art/Planet-EARTH-311255741
        'Planet - Earth' by ulimann644
    """
    earthImage = pg.transform.scale(earthImage, (100, 70))
    earthRect = earthImage.get_rect(center=(900,150))
    
    backgroundImage = pg.image.load("backgroundStars.png")
    # Image Source: http://pluspng.com/stars-png-hd-8254.html
    backgroundImage = pg.transform.scale(backgroundImage, (width, height))
    
    while True:
        currentMode = startMenu()
        
        while currentMode != "Start Menu":
            if currentMode == "Free Play":
                currentMode = freePlayMenu()
                if currentMode == "Host":
                    currentMode = hostGame()
                elif currentMode == "Join":
                    currentMode = joinedGame()
            elif currentMode == "Classic Mode":
                currentMode = classicMode()
            elif currentMode == "Frenzy Mode":
                currentMode = frenzyMode()
            elif currentMode == "How To Play":
                currentMode = howToPlayScreen()
        
if __name__ == '__main__':
    main()
        
        
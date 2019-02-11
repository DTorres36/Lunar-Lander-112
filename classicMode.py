#################################################################
# Lunar Lander 112 V1.3 - Classic Mode
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## classic mode file: runs classic mode

import pygame as pg
from spriteClasses import *
import sys
from mapLists import classicMapList
from shapely.geometry import Polygon

pg.init()

size = width, height = 1000, 700
pg.display.set_caption("Lunar Lander 112")
screen = pg.display.set_mode(size)
screenRect = screen.get_rect(topleft = (0,0))
clock = pg.time.Clock()

earthImage = pg.image.load("darkEarth.png")
earthImage = pg.transform.scale(earthImage, (100, 70))
earthRect = earthImage.get_rect(center=(900,150))

backgroundImage = pg.image.load("backgroundStars.png")
backgroundImage = pg.transform.scale(backgroundImage, (width, height))

def landCondition(lander, mapPolygon, flatSurfaces):
    if lander.polygon.intersects(mapPolygon):
        for surface in flatSurfaces:
            start, end = surface
            if lander.x - 25 > start and lander.x + 25 < end and \
            lander.safeToLand(True):
                return "SAFE"
        return "CRASH"
    return None

def safeMessage(lander, points):
    message = "Nice Landing! %d points" % points
    font = pg.font.SysFont("arial", 50, True)
    text = font.render(message, True, (255,255,255))
    textRect = text.get_rect(center = 
                        (width//2, height//3))
    screen.blit(text, textRect)

def crashMessage(lander, fuelLost):
    message = "Attempt failed! %d units of fuel lost" % fuelLost
    font = pg.font.SysFont("arial", 50, True)
    text = font.render(message, True, (255,255,255))
    textRect = text.get_rect(center = 
                        (width//2, height//3))
    screen.blit(text, textRect)
    
def pressSpaceText(isGameOver, crashed):
    if isGameOver:
        message = "Press space to return to Main Menu"
    elif crashed:
        message = "Press space to retry"
    else:
        message = "Press space to continue"
    font = pg.font.SysFont("arial", 50, True)
    text = font.render(message, True, (255,255,255))
    textRect = text.get_rect(center = 
                        (width//2, height//2))
    screen.blit(text, textRect)
    
def printLanderData(lander, points):
    speed = (lander.xSpeed**2 + lander.ySpeed**2)**0.5
    font = pg.font.SysFont("arial", 20, True)
    
    topLeftText = ["Fuel: %d" % lander.fuel,
                    "Score: %d" % points]
    for i in range(len(topLeftText)):
        line = topLeftText[i]
        text = font.render(line, True, (255,255,255))
        screen.blit(text, (20, 20 + 20*i))
    
    topRightText = ["Total Speed: %.3f"  % (speed*10),
                    "Horizontal Vel: %.3f" % (lander.xSpeed*10),
                    "Vertical Vel: %.3f" % (lander.ySpeed*10)]
    for i in range(len(topRightText)):
        line = topRightText[i]
        text = font.render(line, True, (255,255,255))
        screen.blit(text, (width - 250, 20 + 20*i))
        
def calculatePoints(lander):
    reward = 0
    if lander.xSpeed > .5:
        reward += 20
    elif lander.xSpeed > .1:
        reward += 30
    else:
        reward += 50
        
    if lander.ySpeed > .5:
        reward += 20
    elif lander.ySpeed > .1:
        reward += 30
    else:
        reward += 50
    
    if lander.angle != 0:
        reward += 30
    else:
        reward += 50

    return reward
        
def calculateFuelLost(lander):
    fuelLost = 0
    if lander.xSpeed > 1:
        fuelLost += 60
    elif lander.xSpeed > .5:
        fuelLost += 40
    else:
        fuelLost += 30
        
    if lander.ySpeed > 2:
        fuelLost += 80
    elif lander.ySpeed > 1:
        fuelLost += 60
    else:
        fuelLost += 30
    
    if -5 < lander.angle < 5:
        fuelLost += 30
    else:
        fuelLost += 60
        
    return fuelLost

def gameOverText(points):
    message = "No More Fuel! Final Score: " + str(points)
    font = pg.font.SysFont("arial", 50, True)
    text = font.render(message, True, (255,255,255))
    textRect = text.get_rect(center = 
                        (width//2, height//3))
    screen.blit(text, textRect)

def classicMode():
    explosionImage = pg.image.load("explosion.png")
    # Image Source: http://clubpenguin.wikia.com/wiki/File:Explode.png
    explosionImage = pg.transform.scale(explosionImage, (150, 100))
    
    lander = Lander()
    mapVertices, flatSurfaces = classicMapList()
    mapPolygon = Polygon(mapVertices)
    points = 0
    pointsCalculated = False
    # pointsCalculated keeps track if new score/fuel has been updated
    isGameOver = False
    while True:
        for event in pg.event.get([pg.QUIT, pg.KEYDOWN]):
            if event.type == pg.QUIT: 
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return "Start Menu"
                else: 
                    pg.event.post(event)
        
        if landCondition(lander, mapPolygon, flatSurfaces) != None:
            attemptOver = True
            if landCondition(lander, mapPolygon, flatSurfaces) == "CRASH":
                crashed = True
        else:
            attemptOver = False
            crashed = False
            
        if attemptOver:
            # lander has reached the ground
            if not pointsCalculated:
                # points are updated
                if landCondition(lander, mapPolygon, flatSurfaces) == "SAFE":
                    rewardedPoints = calculatePoints(lander)
                    points += rewardedPoints
                else:
                    fuelLost = calculateFuelLost(lander)
                    lander.fuel -= fuelLost
                    if lander.fuel < 0:
                        lander.fuel = 0
                    lander.angle = 90
                lander.xSpeed = 0
                lander.ySpeed = 0
                pointsCalculated = True
            
            # player presses space to reset
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if isGameOver:
                            return "Start Menu"
                        elif lander.fuel == 0:
                            isGameOver = True
                        else:
                            attemptOver = False
                            fuel = lander.fuel
                            pointsCalculated = False
                            lander.__init__()
                            lander.fuel = fuel
                            if not crashed:
                                mapVertices, flatSurfaces = classicMapList()
                                mapPolygon = Polygon(mapVertices)
                            crashed = False
        else:
            # Normal Gameplay
            lander.ySpeed += .005
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        lander.boosting = True
                    elif event.key == pg.K_LEFT:
                        lander.angleChange = 3
                    elif event.key == pg.K_RIGHT:
                        lander.angleChange = -3
                elif event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        lander.boosting = False
                    elif event.key == pg.K_LEFT:
                        lander.angleChange = 0
                    elif event.key == pg.K_RIGHT:
                        lander.angleChange = 0
            
            if lander.boosting == True:
                lander.boost()
        
        ## Display updates ##
        lander.updatePosition()
        lander.updateAngle(True)

        screen.blit(backgroundImage, screenRect)
        screen.blit(earthImage, earthRect)
        lander.updateImage(screen)
        pg.draw.polygon(screen, (150, 150, 150), mapVertices) # map
        printLanderData(lander, points)
            
        if attemptOver:
            if crashed:
                screen.blit(explosionImage, (lander.x - 75, lander.y - 50))
            if isGameOver:
                gameOverText(points)
            elif not crashed:
                safeMessage(lander, rewardedPoints)
            else:
                crashMessage(lander, fuelLost)
            pressSpaceText(isGameOver, crashed)
            
        pg.display.flip()
        pg.display.update()
        clock.tick(35)
    
if __name__ == '__main__':
    classicMode()
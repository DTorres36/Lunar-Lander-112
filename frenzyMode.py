#################################################################
# Lunar Lander 112 V1.3 - Frenzy Mode
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## frenzy mode file: runs frenzy mode

import pygame as pg
from spriteClasses import *
import sys
from mapLists import mapGen
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

def meteorCrash(lander, meteorList):
    for meteor in meteorList:
        if lander.polygon.intersects(meteor.polygon):
            return True
    return False

def missileHit(lander, missileList):
    for missile in missileList:
        if lander.polygon.contains(missile.centerPoint):
            return True
    return False

def landCondition(lander, mapPolygon, flatSurfaces):
    if lander.polygon.intersects(mapPolygon):
        for surface in flatSurfaces:
            start, end = surface
            if lander.x - 25 > start and lander.x + 25 < end and \
            lander.safeToLand():
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

def timesUpMessage():
    message = "Time's Up! 350 units of fuel lost!"
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
    
def printLanderData(lander, points, timeLeft):
    speed = (lander.xSpeed**2 + lander.ySpeed**2)**0.5
    font = pg.font.SysFont("arial", 20, True)
    
    topLeftText = ["Fuel: %d" % lander.fuel,
                    "Score: %d" % points,
                    "Time Left: %d" % timeLeft]
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
        
def calculateFuelLost(lander, timesUp):
    fuelLost = 0
    if timesUp:
        fuelLost = 350
    else:
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

def frenzyMode():
    explosionImage = pg.image.load("explosion.png")
    # Image Source: http://clubpenguin.wikia.com/wiki/File:Explode.png
    explosionImage = pg.transform.scale(explosionImage, (150, 100))
    
    lander = Lander()
    lander.__init__(True)
    lander.fuel = 4000
    meteorList = []
    enemyList = []
    missileList = []
    mapVertices, flatSurfaces = mapGen()
    mapPolygon = Polygon(mapVertices)
    points = 0
    pointsCalculated = False
    # pointsCalculated keeps track if new score/fuel has been updated
    isGameOver = False
    timeLeft = 15
    timesUp = False
    tick = 0
    fps = 35
    while True:        
        for event in pg.event.get([pg.QUIT, pg.KEYDOWN]):
            if event.type == pg.QUIT: 
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    return "Start Menu"
                else:
                    pg.event.post(event)
            
        if landCondition(lander, mapPolygon, flatSurfaces) != None or \
        meteorCrash(lander, meteorList) or missileHit(lander, missileList) or \
            timesUp:
            attemptOver = True
            if landCondition(lander, mapPolygon, flatSurfaces) != "SAFE":
                crashed = True
        else:
            attemptOver = False
            crashed = False
        
        if not attemptOver:
            tick += 1
            if tick % fps == 0:
                timeLeft -= 1
                if timeLeft == 0:
                    timesUp = True
            if tick % 70 == 0 and tick > 70:
                meteor = Meteor()
                meteorList += [meteor]
                if tick % 140 == 0:
                    enemy = Enemy()
                    enemyList += [enemy]
            for enemy in enemyList:
                missile = enemy.fireMissile(enemy, lander)
                if missile != None:
                    missileList += [missile]
                
        if attemptOver:
            # lander has reached the ground
            if not pointsCalculated:
                # points are updated
                if landCondition(lander, mapPolygon, flatSurfaces) == "SAFE":
                    rewardedPoints = calculatePoints(lander)
                    points += rewardedPoints
                else:
                    fuelLost = calculateFuelLost(lander, timesUp)
                    lander.fuel -= fuelLost
                    if lander.fuel < 0:
                        lander.fuel = 0
                    lander.angle = 90
                lander.angleChange = 0
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
                            tick = 0
                            timeLeft = 15
                            timesUp = False
                            attemptOver = False
                            meteorList = []
                            enemyList = []
                            missileList = []
                            fuel = lander.fuel
                            pointsCalculated = False
                            lander.__init__(True)
                            lander.fuel = fuel
                            if not crashed:
                                mapVertices, flatSurfaces = mapGen()
                                mapPolygon = Polygon(mapVertices)
                            crashed = False
        else:
            # Normal Gameplay
            lander.ySpeed += .01
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
                lander.boost()
                lander.boost()
        
        ## Display updates ##
        lander.updatePosition()
        lander.updateAngle()
        # 360 degrees of rotation!
       
        screen.blit(backgroundImage, screenRect)
        screen.blit(earthImage, earthRect)
        lander.updateImage(screen)
        pg.draw.polygon(screen, (150, 150, 150), mapVertices) # map
        printLanderData(lander, points, timeLeft)
        
        toBeRemoved = set()
        for enemy in enemyList:
            if not attemptOver:
                if enemy.updatePosition() == "OUT OF BOUNDS":
                    toBeRemoved.add(enemy)
                    continue
            screen.blit(enemy.image, enemy.rect)
        for enemy in toBeRemoved: enemyList.remove(enemy)
        toBeRemoved.clear()
        
        for meteor in meteorList:
            if not attemptOver:
                if meteor.updatePosition() == "OUT OF BOUNDS" or \
                    meteor.polygon.intersects(mapPolygon):
                    toBeRemoved.add(meteor)
                    continue
            screen.blit(meteor.image, meteor.rect)
        for meteor in toBeRemoved: meteorList.remove(meteor)
        toBeRemoved.clear()
        
        for missile in missileList:
            if not attemptOver:
                if missile.updatePosition() == "OUT OF BOUNDS" or \
                    mapPolygon.contains(missile.centerPoint):
                    toBeRemoved.add(missile)
                    continue
            screen.blit(missile.image, missile.rect)
        for missile in toBeRemoved: missileList.remove(missile)
        
        if attemptOver:
            if crashed:
                screen.blit(explosionImage, (lander.x - 75, lander.y - 50))
            if isGameOver:
                gameOverText(points)
            elif not crashed:
                safeMessage(lander, rewardedPoints)
            elif not timesUp:
                crashMessage(lander, fuelLost)
            else:
                timesUpMessage()
            pressSpaceText(isGameOver, crashed)
            
        pg.display.flip()
        pg.display.update()
        clock.tick(fps)
    
if __name__ == '__main__':
    frenzyMode()
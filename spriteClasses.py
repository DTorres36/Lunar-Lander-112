#################################################################
# Lunar Lander 112 V1.3 - spriteClasses
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## sprites file: each sprite/class used in the game is stored in this file

import pygame as pg
import math
import shapely
# implemented with help from offical shapely documentation site
# https://shapely.readthedocs.io/en/stable/manual.html
# used in collision detection between sprites and the surface.
from shapely.geometry import Polygon, Point
import random

class Lander(pg.sprite.DirtySprite):
    def __init__(self, isFrenzyMode = False):
        if isFrenzyMode:
            self.x = random.randint(50, 950)
            self.y = random.randint(50, 75)
            self.ySpeed = random.uniform(-0.5, 0.1)
            if self.x < 500:
                self.xSpeed = random.uniform(1, 3)
                self.angle = 90
            else:
                self.xSpeed = random.uniform(-3, -1)
                self.angle = -90
            topLeft = (self.x - 25, self.y - 25)
            topRight = (self.x + 25, self.y - 25)
            botLeft = (self.x - 25, self.y + 25)
            botRight = (self.x + 25, self.y + 25)
            self.polygon = Polygon([topLeft, topRight, botRight, botLeft])
        else:
            self.x = 50
            self.y = 50
            self.polygon = Polygon([(25, 25), (25, 75), (75, 75), (75, 25)])
            self.xSpeed = 1.5
            self.ySpeed = 0
            self.angle = 90
        self.angleChange = 0
        self.fuel = 2000
        self.boosting = False
        self.exhaustDistance = 40
        # distance between center of lander image and center of exhaust image
        
        exhaustImage = pg.image.load("landerExhaust.png")
        # Image Source: https://es.vexels.com/png-svg/vista-previa/145659/dibujo-animado-de-la-llama
        landerImage = pg.image.load("lunarLander.png")
        # Image Source: https://www.kisspng.com/png-lunar-lander-computer-icons-spacecraft-2105265/
        self.originalExhaustImage = pg.transform.scale(exhaustImage, (50, 50))
        self.originalImage = pg.transform.scale(landerImage, (50, 50))
        # original image is preserved to perform clean rotations
        # continuously rotating an image causes distortions
        self.exhaustImage = self.originalExhaustImage
        self.image = self.originalImage
        
    def boost(self):
        deltaV = .012
        if self.fuel == 0:
            return None
        deltaXSpeed = deltaV*math.cos(math.radians(self.angle+90))
        self.xSpeed += deltaXSpeed
        deltaYSpeed = deltaV*math.sin(math.radians(self.angle+90))
        self.ySpeed -= deltaYSpeed
        self.fuel -= 1
    
    def updatePosition(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.polygon = shapely.affinity.translate(self.polygon, self.xSpeed, 
                self.ySpeed)
        if self.x < 25:
            self.x = 25
            self.xSpeed = 0
        elif self.x > 975:
            self.x = 975
            self.xSpeed = 0
        
    def updateAngle(self, isClassicMode=False):
        self.angle += self.angleChange
        self.polygon = shapely.affinity.rotate(self.polygon, self.angleChange)
        if isClassicMode:
            if self.angle > 90:
                self.angle = 90
                self.angleChange = 0
            elif self.angle < -90:
                self.angle = -90
                self.angleChange = 0
            
    def updateImage(self, screen):
        rectCenter = self.x, self.y
        self.image = pg.transform.rotate(self.originalImage, 
                                        self.angle)
        self.rect = self.image.get_rect(center = rectCenter)
        
        d = self.exhaustDistance
        exhaustX = self.x + d*math.sin(math.radians(self.angle))
        exhaustY = self.y + d*math.cos(math.radians(self.angle))
        rectCenter = exhaustX, exhaustY
        self.exhaustImage = pg.transform.rotate(self.originalExhaustImage,
                                        self.angle + 180)
        self.exhaustRect = self.exhaustImage.get_rect(center = rectCenter)
        
        if self.boosting == True and self.fuel != 0:
            screen.blit(self.exhaustImage, self.exhaustRect)
        screen.blit(self.image, self.rect)
        
    def safeToLand(self, isClassicMode=False):
        v = (self.xSpeed**2 + self.ySpeed**2)**0.5
        if isClassicMode:
            if -6 <= self.angle <= 6 and v < 1:
                return True
        else:
            if -6 <= self.angle % 360 <= 6 and v < 1.5:
                return True
        return False
        
class Enemy(pg.sprite.DirtySprite):
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = random.choice([-self.width/2, 1000 + self.width/2])
        self.y = random.randint(50, 150)
        if self.x < 0:
            self.xSpeed = random.randint(2, 4)
        else:
            self.xSpeed = random.randint(-4, -2)
        self.ySpeed = random.uniform(-0.05, 0.05)
        enemyImage = pg.image.load("enemyUFO.png")
        # Image Source: https://www.kisspng.com/png-unidentified-flying-object-flying-saucer-cartoon-c-79268/preview.html
        self.image = pg.transform.scale(enemyImage, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.x, self.y))
        
        self.tick = 0
        
    def updatePosition(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        rectCenter = self.x, self.y
        self.rect = self.image.get_rect(center = rectCenter)
        if self.x < -self.width/2 or self.x > 1000 + self.width/2:
            return "OUT OF BOUNDS"
    
    def fireMissile(self, enemy, lander):
        self.tick += 1
        if self.tick % 45 == 0:
            return Missile(enemy, lander)
        
class Missile(pg.sprite.DirtySprite):
    def __init__(self, enemy, lander):
        self.x = enemy.x
        self.y = enemy.y
        self.centerPoint = Point((self.x, self.y))
        targetX, targetY = lander.x + 10*lander.xSpeed, lander.y + 10*lander.ySpeed
        heightDif = targetY - self.y
        widthDif = targetX - self.x
        angle = math.atan2(heightDif, widthDif)
        speed = random.randint(3, 5)
        self.xSpeed = speed*math.cos(angle)
        self.ySpeed = speed*math.sin(angle)
        
        angle = -90 - math.degrees(angle) 
        missileImage = pg.image.load("missileImage.png")
        # Image Source: 
        missileImage = pg.transform.scale(missileImage, (20, 20))
        self.image = pg.transform.rotate(missileImage, angle)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        
    def updatePosition(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        rectCenter = self.x, self.y
        self.rect = self.image.get_rect(center = rectCenter)
        self.centerPoint = shapely.affinity.translate(self.centerPoint, 
            self.xSpeed, self.ySpeed)
        if self.x < -10 or self.x > 1010:
            return "OUT OF BOUNDS"

class Meteor(pg.sprite.DirtySprite):
    def __init__(self):
        self.x = random.randint(0, 1000)
        self.y = 0
        self.width = 75
        self.height = 60
        self.xSpeed = random.randint(-3, 3)
        self.ySpeed = random.randint(3, 5)
        orientation = random.randint(0, 360)
        polygon = Polygon([(self.x - self.width/2, self.y - self.height/2), 
                        (self.x + self.width/2, self.y - self.height/2), 
                        (self.x + self.width/2, self.y + self.height/2), 
                        (self.x - self.width/2, self.y + self.height/2)])
        meteorImage = pg.image.load("meteor.png")
        # image source: https://vignette.wikia.nocookie.net/scribblenauts/images/a/aa/Meteor_HD.png/revision/latest/scale-to-width-down/135?cb=20121228002932
        meteorImage = pg.transform.scale(meteorImage, (self.width, self.height))
        self.image = pg.transform.rotate(meteorImage, orientation)
        self.rect = self.image.get_rect(center = (self.x, self.y))
        self.polygon = shapely.affinity.rotate(polygon, orientation)
        
    def updatePosition(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        rectCenter = self.x, self.y
        self.rect = self.image.get_rect(center = rectCenter)
        self.polygon = shapely.affinity.translate(self.polygon, self.xSpeed, 
                self.ySpeed)
        if self.x < -self.width/2 or self.x > 1000 + self.width/2:
            return "OUT OF BOUNDS"
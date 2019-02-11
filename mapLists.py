#################################################################
# Lunar Lander 112 V1.3 - mapLists
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## maps file: this file contains the designs of the classic maps as well as the map generation algorithm used in frenzy

import pygame as pg
from shapely.geometry import Polygon
import random

mapSegments = [(30, 100), (50, 100), (60, 100), (70, 100), (80, 100), (90, 100),
                (200, 100), (300, 100), (30, 50), (60, 50), (100, 50), (150, 50),
                (10, 200), (30, 200), (50, 200), (70, 200), (120, 200), (150, 200),
                (30, 300), (50, 300), (70, 300), (120, 300), (170, 200), (250, 300),
                (15, 400), (30, 400), (60, 400), (90, 400), (140, 400)]

flatPieces = [(0, 70), (70, 130), (130, 190), (190, 300), (300, 370), 
                (370, 500), (500, 560), (560, 630), (630, 710), (710, 790),
                (790, 860), (860, 930)]
                
flatDists = [60]*5 + [70]*8 + [80]*4 + [90]*3 + [100]*2 + [120]*2 + [150]*2 + [190] + [230]
                
def mapGen():
    numOfFlats = random.randint(1, 4)
    flatRanges = []
    # ranges that in game flats are based off
    availableFlats = flatPieces[::]
    # flats left to choose from
    while len(flatRanges) < numOfFlats:
        range = random.choice(availableFlats)
        availableFlats.remove(range)
        flatRanges += [range]
    
    prevX = 0
    prevY = random.randint(100, 650)
    length = 0
    map = [(prevX, prevY)]
    actualFlats = []
    # the flat surfaces actually seen in game
    while length < 1000:
        flatChosen = False
        for range in flatRanges:
            if range[0] < length <= range[1]:
                dist = random.choice(flatDists)
                nextX = prevX + dist
                nextY = prevY
                actualFlats += [(prevX, nextX)]
                flatRanges.remove(range)
                flatChosen = True
                break
        if flatChosen:
            map += [(nextX, nextY)]
        else:
            while True:
                nextPiece = random.choice(mapSegments)
                direction = random.choice([-1, 1])
                dY = nextPiece[1]
                if 150 < prevY + dY*direction < 650:
                    break
            dX = nextPiece[0]
            nextX = prevX + dX
            nextY = prevY + dY*direction
            map += [(nextX, nextY)]
        prevX, prevY = nextX, nextY
        length = nextX
    if len(actualFlats) == 0:
        while length > 930:
            map.pop()
            length = map[-1][0]
        prevX, prevY = map[-1]
        nextX, nextY = 1000, prevY
        actualFlats += [(prevX, nextX)]
        map += [(nextX, nextY)]
    map += [(nextX, 700), (0, 700)]
    return map, actualFlats

def classicMapList():
    maps = [[(0, 500), (300, 600), (500, 600), (1000, 500), (1000, 700), 
                (0, 700)],
            [(0, 600), (200, 650), (400, 350), (500, 450), (600, 450),
                (800, 500), (1000, 200), (1000, 700), (0, 700)],
            [(0, 300), (100, 400), (200, 500), (290, 500), (350, 200),
                (500, 150), (600, 400), (800, 400), (1000, 600), (1000, 700),
                (0, 700)],
            [(0, 700), (50, 650), (100, 630), (200, 400), (400, 200),
                (450, 300), (500, 350), (700, 450), (780, 450), (880, 550),
                (980, 550), (1000, 400), (1000, 700), (0, 700)],
            [(0, 200), (100, 250), (200, 350), (300, 500), (400, 690), 
                (470, 690), (550, 450), (700, 300), (1000, 200), (1000, 700),
                (0, 700)],
            [(0, 600), (100, 650), (300, 650), (350, 400), (600, 300),
                (700, 500), (900, 500), (1000, 600), (1000, 700), (0, 700)],
            [(0, 400), (50, 600), (200, 690), (500, 300), (550, 250),
                (630, 250), (700, 200), (850, 500), (1000, 600), (1000, 700),
                (0, 700)],
            [(0, 690), (200, 650), (300, 300), (500, 100), (550, 350),
                (600, 500), (670, 500), (800, 550), (1000, 600), (1000, 700),
                (0, 700)],
            [(0, 600), (100, 600), (200, 350), (300, 250), (390, 200), 
                (500, 250), (400, 450), (480, 600), (600, 690), (670, 690), 
                (850, 500), (900, 300), (850, 200), (700, 100), (600, 150), 
                (550, 150), (625, 50), (700, 0), (1000, 0), (1000, 700), 
                (0, 700)],
            [(0, 450), (100, 500), (150, 600), (300, 450), (360, 450),
                (400, 475), (500, 350), (600, 325), (750, 200), (950, 200),
                (1000, 50), (1000, 700), (0, 700)]]
    flatList = [[(300, 500)], [(500, 600)], [(200, 290), (600, 800)],
                [(700, 780), (880, 980)], [(400, 470)], 
                [(100, 300), (700, 900)], [(550, 630)], [(600, 670)],
                [(0, 100), (600, 700)], [(300, 360), (750, 950)]]
    choice = random.randint(0, 9)
    vertices = maps[choice]
    flatSurfaces = flatList[choice]
    return vertices, flatSurfaces
    
if __name__ == "__main__":
    mapGen()
    
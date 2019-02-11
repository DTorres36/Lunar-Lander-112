#################################################################
# Lunar Lander 112 V1.3  - joinedPlayer
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## joined player file for free play: runs free play mode as a player connected to a host

import socket
import pickle
# sockets and pickle implemented with help from official Python Documentation page
# used in the transmission of data between players in free play
# sockets: https://docs.python.org/3/library/socket.html
# pickle: https://docs.python.org/3/library/pickle.html
import pygame as pg
import sys
from spriteClasses import *
from menuScreen import enterHostInfo

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

def gamePlay(lander):
    for event in pg.event.get([pg.QUIT, pg.KEYDOWN]):
        if event.type == pg.QUIT: 
            return "quit"
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                return "Start Menu"
            else: 
                pg.event.post(event)
    
        # Normal Gameplay
    lander.ySpeed += .01
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                lander.boosting = True
            elif event.key == pg.K_LEFT:
                lander.angleChange = 5
            elif event.key == pg.K_RIGHT:
                lander.angleChange = -5
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
        lander.boost()
        lander.boost()
        lander.fuel = 1000
    
    # Display updates #
    lander.updatePosition()
    lander.updateAngle()
    if lander.y > 575:
        lander.y = 575
        lander.ySpeed = 0

    screen.blit(backgroundImage, screenRect)
    screen.blit(earthImage, earthRect)
    lander.updateImage(screen)
    pg.draw.rect(screen, (200,200,200), (0, 600, width, 100))
    clock.tick(30)
    
def errorScreen():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return "quit"
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return "Start Menu"
        screen.blit(backgroundImage, screenRect)
        
        # title
        titleFont = pg.font.SysFont("courier new", 50, True)
        titleTextTop = titleFont.render("Disconnected from Host", True, 
                (200,10,10))
        titleTextBottom = titleFont.render("Press space to return to menu", 
                True, (150,150,150))
        titleTextTopRect = titleTextTop.get_rect(center = (width//2, height//3))
        titleTextBottomRect = titleTextBottom.get_rect(center = (width//2, 
            2*height//3))
        screen.blit(titleTextTop, titleTextTopRect)
        screen.blit(titleTextBottom, titleTextBottomRect)        
            
        pg.display.flip()
        pg.display.update()
    
def displayServerInfo(server):
    font = pg.font.SysFont("arial", 20, True)
    serverInfo = "Host Address: %s, Port %d" % (server[0], server[1])
    text = font.render(serverInfo, True, (200,200,200))
    screen.blit(text, (20, 20))
    
def joinedGame():
    # Setup framework based off https://realpython.com/python-sockets/
    userLander = Lander()
    hostLander = Lander()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    playerAddress = ('127.0.0.1', 0)
    s.bind(playerAddress)
    s.setblocking(0)
    
    connected = False
    failedConnection = False
    quitting = False
    while connected == False:
        try:
            hostInfo = enterHostInfo(failedConnection)
            if hostInfo == "Free Play":
                s.close()
                return "Free Play"
            elif hostInfo == "exit":
                s.close()
                quitting = True
            hostIP, hostPort = hostInfo
            server = (hostIP, hostPort)
            s.sendto("boop".encode('utf-8'), server)
            connected = True
        except:
            failedConnection = True
        if quitting == True:
            sys.exit()
                
    while connected == True:
        if gamePlay(userLander) != None:
            encodedData = "quit".encode('utf-8')
            s.sendto(encodedData, server)
            s.close()
            if gamePlay(userLander) == "Start Menu":
                return "Start Menu"
            else:
                sys.exit()
            
        userLocation = (userLander.x, userLander.y, userLander.angle)
        encodedData = pickle.dumps(userLocation)
        s.sendto(encodedData, server)
        try:
            incoming, address = s.recvfrom(1024)
            hostLocation = pickle.loads(incoming)
            hostLander.x, hostLander.y, hostLander.angle = hostLocation
            hostLander.updateImage(screen)
        except:
            try:
                if incoming.decode('utf-8') == "quitting":
                    s.close()
                    errorReturn = errorScreen()
                    if errorReturn == "quit":
                        quitting = True
                    else:
                        return errorReturn
            except:
                pass
            if quitting == True:
                sys.exit()

                
        displayServerInfo(server)
        pg.display.flip()
        pg.display.update()

    
if __name__ == '__main__':
    joinedGame()
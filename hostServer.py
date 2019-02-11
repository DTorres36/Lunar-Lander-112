#################################################################
# Lunar Lander 112 V1.3  - hostPlayer
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## host/solo file for free play: runs free play mode as host

import socket
import pickle
# sockets and pickle implemented with help from official Python Documentation page
# used in the transmission of data between players in free play
# sockets: https://docs.python.org/3/library/socket.html
# pickle: https://docs.python.org/3/library/pickle.html
import pygame as pg
import sys
from spriteClasses import *

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

    screen.blit(backgroundImage, screenRect)
    screen.blit(earthImage, earthRect)
    lander.updateImage(screen)
    pg.draw.rect(screen, (200,200,200), (0, 600, width, 100))
    if lander.y > 575:
            lander.y = 575
            lander.ySpeed = 0
        
    clock.tick(30)
    
def displayServerInfo(sock):
    font = pg.font.SysFont("arial", 20, True)
    host, port = sock.getsockname()
    serverInfo = "Host Address: %s, Port %d" % (host, port)
    text = font.render(serverInfo, True, (200,200,200))
    screen.blit(text, (20, 20))
        
def hostGame():
    # Setup framework based off https://realpython.com/python-sockets/
    hostLander = Lander()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    host = socket.gethostbyname(socket.gethostname())
    port = 5000
    s.bind((host, port))
    s.setblocking(0)
    
    print("Server Started")
    
    clients = set()
    
    while True:   
        gameState = gamePlay(hostLander)
        if gameState != None:
            print("Server Closed")
            for client in clients:
                s.sendto("quitting".encode('utf-8'), client)
            s.close()
            if gameState == "Start Menu":
                return "Start Menu"
            else:
                sys.exit()
        
        hostLocation = (hostLander.x, hostLander.y, hostLander.angle) 
        encodedData = pickle.dumps(hostLocation)
        for client in clients:
            s.sendto(encodedData, client)
        try:
            incoming, address = s.recvfrom(1024)
            if address not in clients:
                clients.add(address)
                playerLander = Lander()
                continue
            try:
                if playerLocation.decode('utf-8') == "quit":
                    clients.remove(address)
            except:
                playerLocation = pickle.loads(incoming)
            
            playerLander.x, playerLander.y, playerLander.angle = \
                playerLocation
            playerLander.updateImage(screen)
            for client in clients:
                if client != address:
                    s.sendto(hostLocation, client)
        except:
            pass
        
        displayServerInfo(s)
        pg.display.flip()
        pg.display.update()
    
if __name__ == '__main__':
    hostGame()
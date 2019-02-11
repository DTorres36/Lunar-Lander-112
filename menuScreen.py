#################################################################
# Lunar Lander 112 V1.3  - menuScreen
# Name: Darwin Torres
# Andrew ID: dtorresr
# Section: L
#################################################################

## UI File: Most of the UI is implemented here

import pygame as pg
import sys

pg.init()

size = width, height = 1000, 700
screen = pg.display.set_mode(size)
screenRect = screen.get_rect(topleft = (0,0))
clock = pg.time.Clock()

backgroundImage = pg.image.load("backgroundStars.png")
backgroundImage = pg.transform.scale(backgroundImage, (width, height))

def createButton(gamemode, left, top, buttonWidth=300, buttonHeight=100):
    buttonFont = pg.font.SysFont("arial", 25)
    mouseX, mouseY = pg.mouse.get_pos()
    leftClick = pg.mouse.get_pressed()[0]
    
    if left < mouseX < left + buttonWidth and \
        top < mouseY < top + buttonHeight:
        color = (75,75,75)
        if leftClick == 1:
            return gamemode
    else: color = (50,50,50)
    
    buttonRect = pg.draw.rect(screen, color, 
        (left, top, buttonWidth, buttonHeight))
    pg.draw.rect(screen, (255,255,255), 
        (left, top, buttonWidth, buttonHeight), 2)
    text = buttonFont.render(gamemode, True, (150,150,150))
    textRect = text.get_rect(center = 
                        (left + buttonWidth//2, top + buttonHeight//2))
    screen.blit(text, textRect)
    
def howToPlayScreen():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                sys.exit()
        screen.blit(backgroundImage, screenRect)
        pg.draw.rect(screen, (100, 100, 100), 
                (width//10, height//15, 8*width//10, 7*height//10))
        pg.draw.rect(screen, (255, 255, 255), 
                (width//10, height//15, 8*width//10, 7*height//10), 1)
                
        font = pg.font.SysFont("arial", 20, True)
        topLeftText = ["Basic Lander Controls",
                        "       Left and Right arrows keys control angle",
                        "       Up arrow key activates booster",
                        "       Return to menu by pressing 'q' while in game",
                        "Classic Mode",
                        "       Land the lander on a flat, level surface!",
                        "       Low speed and upright angle is key!",
                        "Frenzy Mode",
                        "       More challenging and faster paced!",
                        "       Watch out for enemy missiles and falling meteors!",
                        "       Timing is crucial! Watch the clock in this mode!",
                        "       Extra kick added to gravity and boosting, harder landings allowed!",
                        "       Lander has no angle restrictions, and extra fuel!",
                        "       Maps are randomly generated!",
                        "Free Play",
                        "       No objective, just fly around!",
                        "       Stronger gravity and boosts, and infinite fuel!"]
        for i in range(len(topLeftText)):
            line = topLeftText[i]
            text = font.render(line, True, (230,230,230))
            screen.blit(text, (width//5, height//10 + 25*i))
        
        # Back Button
        backLeft = width//2 - 150
        backTop = height - 125
        backButton = createButton("Back", backLeft, backTop, 300, 100)
        if backButton != None:
            return "Start Menu"
        
        pg.display.flip()
        pg.display.update()
        clock.tick(30)

def enterHostInfo(failed = False):
    buttonWidth = 300
    buttonHeight = 100
    name = ""
    font = pg.font.Font(None, 50)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return "exit"
            # code for displaying user keyboard input is a modified version of code from following source
            # source: https://stackoverflow.com/questions/14111381/how-to-get-text-input-from-user-in-pygame
            if event.type == pg.KEYDOWN:
                name += event.unicode
                if event.key == pg.K_BACKSPACE:
                    name = name[:-2]
                elif event.key == pg.K_RETURN:
                    i = name.find(" ")
                    ip = name[:i]
                    port = int(name[i+1:])
                    return (ip, port)
                        

        screen.blit(backgroundImage, screenRect)
        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        
        # title
        titleFont = pg.font.SysFont("courier new", 80, True, True)
        titleTextTop = titleFont.render("FREE PLAY", True, (150,150,150))
        titleFont = pg.font.SysFont("courier new", 30, True)
        titleTextBottom = titleFont.render("Enter Host IP and Port separated by space", True, (150,150,150))
        titleTextTopRect = titleTextTop.get_rect(center = (width//2, height//8))
        titleTextBottomRect = titleTextBottom.get_rect(center = (width//2, 
            height//4))
        screen.blit(titleTextTop, titleTextTopRect)
        screen.blit(titleTextBottom, titleTextBottomRect)
        
        # error message
        if failed:
            text = font.render("Connection Failed", True, 
                    (200, 10, 10))          
            textRect = text.get_rect(center = (width//2, height//3))
            screen.blit(text, textRect)
            
        # Back Button
        backLeft = width//2 - 150
        backTop = height - 125
        backButton = createButton("Back", backLeft, backTop, 300, 100)
        if backButton != None:
            return "Free Play"
            
            
        pg.display.flip()
        pg.display.update()
        clock.tick(30)
    
def freePlayMenu():
    buttonWidth = 300
    buttonHeight = 100
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                sys.exit()
        screen.blit(backgroundImage, screenRect)
        
        # title
        titleFont = pg.font.SysFont("courier new", 80, True)
        titleTextTop = titleFont.render("FREE PLAY", True, (150,150,150))
        titleTextBottom = titleFont.render("Host, join?", True, (150,150,150))
        titleTextTopRect = titleTextTop.get_rect(center = (width//2, height//8))
        titleTextBottomRect = titleTextBottom.get_rect(center = (width//2, 
            height//4))
        screen.blit(titleTextTop, titleTextTopRect)
        screen.blit(titleTextBottom, titleTextBottomRect)
        
        # Host button
        hostLeft = buttonWidth//2
        hostTop = height//2
        hostButton = createButton("Host / Solo", hostLeft, hostTop)
        if hostButton != None:
            return "Host"
        
        # Join Button
        joinLeft = width - 3*buttonWidth//2
        joinTop = height//2
        joinButton = createButton("Join", joinLeft, joinTop)
        if joinButton != None:
            return joinButton
            
        # Back Button
        backLeft = buttonWidth//2
        backTop = height - buttonHeight
        backButton = createButton("Back", backLeft, backTop, 100, 50)
        if backButton != None:
            return "Start Menu"
            
        pg.display.flip()
        pg.display.update()
        clock.tick(30)
        
def startMenu():
    
    buttonWidth = 300
    buttonHeight = 100    
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                sys.exit()
        screen.blit(backgroundImage, screenRect)
        
        # title
        titleFont = pg.font.SysFont("courier new", 100, True, True)
        titleTextTop = titleFont.render("LUNAR LANDER", True, (150,150,150))
        titleTextBottom = titleFont.render("112", True, (150,150,150))
        titleTextTopRect = titleTextTop.get_rect(center = (width//2, height//8))
        titleTextBottomRect = titleTextBottom.get_rect(center = (width//2, 
            height//4))
        screen.blit(titleTextTop, titleTextTopRect)
        screen.blit(titleTextBottom, titleTextBottomRect)
        
        # my name lol
        font = pg.font.SysFont("arial", 20, True)
        text = font.render("Darwin Torres Romero, dtorresr, 15-112 Section L", True, (250,250,250))
        textRect = text.get_rect(center = (width//4, height - 20))
        screen.blit(text, textRect)
        
        # classic mode button
        classicLeft = width//4 - buttonWidth//2
        classicTop = height//2 - buttonHeight//2
        classicButton = createButton("Classic Mode", classicLeft, classicTop)
        if classicButton != None:
            return classicButton

        # free play button
        freePlayLeft = width//2 - buttonWidth//2
        freePlayTop = 2*height//3
        freePlayButton = createButton("Free Play", freePlayLeft, freePlayTop)
        if freePlayButton != None:
            return freePlayButton
            
        # frenzy mode button
        frenzyLeft = 3*width//4 - buttonWidth//2
        frenzyTop = height//2 - buttonHeight//2
        frenzyButton = createButton("Frenzy Mode", frenzyLeft, frenzyTop)
        if frenzyButton != None:
            return frenzyButton
            
        # How To Play Button
        left = width - buttonWidth
        top = height - buttonHeight
        howToPlayButton = createButton("How To Play", left, top, 200, 50)
        if howToPlayButton != None:
            return howToPlayButton
            
        pg.display.flip()
        pg.display.update()
        clock.tick(30)

if __name__ == "__main__":
    howToPlayScreen()
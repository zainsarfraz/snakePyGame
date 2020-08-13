import pygame
import time
import random
import math

pygame.init()

display_width = 500
display_height = 500
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
size_of_block =10
fps = 10


snakeheadImg = pygame.image.load('snakehead.png')
snaketailImg = pygame.image.load('tail.png')
appleImg = pygame.image.load('apple.png')

gameScreen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("MyGame404")
pygame.display.set_icon(snakeheadImg)


def introScreen():
    GameIntro = True
    gameScreen.fill(white)
    while GameIntro == True:
        printMessageOnScreen("Welcome to the Snake Game",red,-50)
        printMessageOnScreen("Press 'Q' to quit or press 'P' to play again ",black,50)
        pygame.display.update()
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                gameClose = True
                gameOver=False
                introScreen=False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    gameClose = True
                    gameOver=False
                    introScreen=False
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    gameClose=False
                    gameOver=False
                    introScreen=False
                    runGame()
    

def getTextSurfAndRect(msg,color):
    font = pygame.font.SysFont("Comicsansms",25)
    textSurface = font.render(msg,True,color)
    return textSurface,textSurface.get_rect()

def printMessageOnScreen(message,color,yDisplay = 0):
    textSurface , textRectangle = getTextSurfAndRect(message,color)
    textRectangle.center = (display_width/2),(display_height/2) + yDisplay
    gameScreen.blit(textSurface,textRectangle)
   

def increaseSnake(snakelist,size_of_block,direction):

   

    if direction == "left":
        head = pygame.transform.rotate(snakeheadImg,90)
    if direction == "right":
        head = pygame.transform.rotate(snakeheadImg,270)
    if direction == "up":
        head = snakeheadImg
    if direction == "down":
        head = pygame.transform.rotate(snakeheadImg,180)

    gameScreen.blit(head,(snakelist[-1][0],snakelist[-1][1]))
    for xy in snakelist[:-1]:
        gameScreen.blit(snaketailImg,(xy[0],xy[1]))
        #pygame.draw.rect(gameScreen,green,(xy[0],xy[1],size_of_block,size_of_block))


def showScore(score):
    font = pygame.font.SysFont("Comicsansms",15)
    textSurface = font.render("Score : "+str(int(score/2)),True,black)
    gameScreen.blit(textSurface,(0,0))


def runGame():
    lead_x_change = 0
    lead_y_change = 0
    randAppleX = random.randrange(0,display_width-size_of_block)
    randAppleY = random.randrange(0,display_height-size_of_block)
    randAppleX = randAppleX-(randAppleX%size_of_block)
    randAppleY = randAppleY - (randAppleY%size_of_block)
    appleThickness = 30
    gameClose = False
    gameOver = False
    clock = pygame.time.Clock()
    lead_x = display_width/2
    lead_y = display_height/2
    snakeLength = 1
    snakelist = []
    snakeheadDirection = "up"
    #main loop
    while not gameClose:

        while gameOver==True:
            gameScreen.fill(white)
            printMessageOnScreen("Game Over",red,-50)
            printMessageOnScreen("Press 'Q' to quit or press 'P' to play again ",black,50)
            pygame.display.update()
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.QUIT:
                    gameClose = True
                    gameOver=False
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameClose = True
                        gameOver=False
                        pygame.quit()
                        quit()

                    if event.key == pygame.K_p:
                        gameClose=False
                        gameOver=False
                        runGame()

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                gameClose = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change= -size_of_block
                    lead_y_change=0
                    snakeheadDirection="left"
                elif event.key==pygame.K_RIGHT:
                    lead_x_change = size_of_block
                    lead_y_change=0
                    snakeheadDirection="right"
                elif event.key==pygame.K_UP:
                    lead_y_change= -size_of_block
                    lead_x_change=0
                    snakeheadDirection="up"
                elif event.key==pygame.K_DOWN:
                    lead_y_change = size_of_block
                    lead_x_change=0
                    snakeheadDirection="down"
            print(lead_x)

            
        lead_x+=lead_x_change
        lead_y+=lead_y_change
        
        #ending game if head hits wall
        if lead_x>= display_width-size_of_block or lead_x< size_of_block or lead_y>=display_height-size_of_block or lead_y<size_of_block:
            gameOver=True    

        #updating game in each iteration
        gameScreen.fill(white)
        #pygame.draw.rect(gameScreen,red,(randAppleX,randAppleY,appleThickness,appleThickness))
        gameScreen.blit(appleImg,(randAppleX,randAppleY))
        #pygame.draw.rect(gameScreen,green,(lead_x,lead_y,size_of_block,size_of_block))

        pygame.display.update()

        snakehead = []
        snakehead.append(lead_x)
        snakehead.append(lead_y)
        snakelist.append(snakehead)

        if len(snakelist)>snakeLength:
            del snakelist[0]

        for eachSegment in snakelist[:-1]:
            if eachSegment ==snakehead:
                gameOver=True

        increaseSnake(snakelist,size_of_block,snakeheadDirection)
        showScore(snakeLength-1)
        pygame.display.update()

        if lead_x>=randAppleX and lead_x <= randAppleX + appleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY + appleThickness:
                randAppleX = random.randrange(0,display_width-size_of_block)
                randAppleY = random.randrange(0,display_height-size_of_block)
                randAppleX = randAppleX-(randAppleX%size_of_block)
                randAppleY = randAppleY - (randAppleY%size_of_block)
                snakeLength+=2


        clock.tick(fps)
    pygame.quit()
    quit()


introScreen()
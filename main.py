import pygame
from copy import deepcopy
import sys
from utility import *

GREEN = (153, 204, 0)
YELLOW = (255, 191, 0)
SELVER = (140, 140, 140)
SNAKE_WIDTH = 12
SNAKE_HEIGHT = 12
SPEED = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hartha')

player1_start_point = (10, 10)
player2_start_point = (780, 580)
clock = pygame.time.Clock()

player1 = Snake(GREEN, 0, SNAKE_WIDTH, SNAKE_HEIGHT, player1_start_point, 1)
player2 = Snake(YELLOW, 0, SNAKE_WIDTH, SNAKE_HEIGHT, player2_start_point, 2)

gameExit = False

while not gameExit:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameExit = True

        elif event.type == pygame.KEYDOWN :

            if event.key == pygame.K_RIGHT :
                if player1.direc != 2 :
                    player1.direc = 1

            elif event.key == pygame.K_LEFT :
                if player1.direc != 1 :
                    player1.direc = 2

            elif event.key == pygame.K_UP :
                if player1.direc != 4 :
                    player1.direc = 3

            elif event.key == pygame.K_DOWN :
                if player1.direc != 3 :
                    player1.direc = 4


    gameDisplay.fill(SELVER)
    player1.move_head(SPEED, SCREEN_WIDTH, SCREEN_HEIGHT)

    pygame.draw.rect(gameDisplay, GREEN, [400, 300, 10, 10])
    gameDisplay.fill(YELLOW, rect=[100,100,12,12])

    for rect in player1.body :
        pygame.draw.rect(gameDisplay, player1.color, [rect.x, rect.y, SNAKE_WIDTH, SNAKE_HEIGHT])


    pygame.display.update()
    clock.tick(15)

pygame.quit()
sys.exit()

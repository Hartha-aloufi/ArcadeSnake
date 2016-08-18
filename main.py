import pygame
from copy import deepcopy
import sys
from utility import *

GREEN = (153, 204, 0)
YELLOW = (255, 191, 0)
SELVER = (140, 140, 140)
RED = (255, 0 , 0)
SNAKE_WIDTH = 12
SNAKE_HEIGHT = 12
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
food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, RED)

gameExit = False

while not gameExit:
    speed = 10

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameExit = True

        elif event.type == pygame.KEYDOWN :

            if event.key == pygame.K_RIGHT :
                if player1.direc != 2 :
                    player1.direc = 1
                    speed = 12

            elif event.key == pygame.K_LEFT :
                if player1.direc != 1 :
                    player1.direc = 2
                    speed = 12

            elif event.key == pygame.K_UP :
                if player1.direc != 4 :
                    player1.direc = 3
                    speed = 12

            elif event.key == pygame.K_DOWN :
                if player1.direc != 3 :
                    player1.direc = 4
                    speed = 12


    gameDisplay.fill(SELVER)
    player1.move_head(speed, SCREEN_WIDTH, SCREEN_HEIGHT)

    if player1.detect_self_collision() :
        player1.color = RED
    else :
        player1.color = GREEN

    if player1.can_eat(food) :
        player1.eat()
        food.calc_new_pos()


    for rect in player1.body :
        pygame.draw.rect(gameDisplay, player1.color, [rect.x, rect.y, SNAKE_WIDTH, SNAKE_HEIGHT])

    pygame.draw.rect(gameDisplay, food.color, [food.rect.x, food.rect.y, food.rect.width, food.rect.height])
    pygame.display.update()
    clock.tick(30)

pygame.quit()
sys.exit()

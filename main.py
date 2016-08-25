import pygame
import sys
from utility import *
from socketIO_client import SocketIO, BaseNamespace
import threading;
import time



WHITE = (255,255,255)
SELVER = (140, 140, 140)
RED = [255, 0 , 0]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GREEN = (153, 204, 0)
gameExit = False
isGameStarted = False


pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hartha')
clock = pygame.time.Clock()


small_font = pygame.font.SysFont('comicsansms', 15)
mid_font = pygame.font.SysFont('comicsansms', 50)
large_font = pygame.font.SysFont('comicsansms', 70)


def text_objects(text, color, size):
    if size == 'small':
        textSurface = small_font.render(text, True, color)
    elif size == 'mid':
        textSurface = mid_font.render(text, True, color)
    else:
        textSurface = large_font.render(text, True, color)

    return textSurface, textSurface.get_rect()

def messege_to_secreen(msg, color, posV, posH, size = 'small'):
    textSurf, textRect = text_objects(msg, color, size)
    v,h =0,0

    if posV == 'top':
        v = 20
    elif posV == 'bottom' :
        v = SCREEN_HEIGHT - 20
    elif posV == 'center' :
        v = SCREEN_HEIGHT / 2

    if posH == 'right':
        h = 50
    elif posH == 'left':
        h = SCREEN_WIDTH - 50
    elif posH == 'center':
        h = SCREEN_WIDTH / 2

    textRect.center = h, v
    gameDisplay.blit(textSurf, textRect)


x = 0

class Namespace(BaseNamespace):
    def on_connect(self):
        print("Connected")

    def on_player_win(self):
        global x, isGameStarted
        msg = 'you win '
        messege_to_secreen(msg, GREEN, 'center', 'center', 'large')
        pygame.display.update()
        time.sleep(3)
        isGameStarted = False
        x = 0
        socketIO.emit('disconnect')

    def on_game_over(self):
        global x, isGameStarted
        msg = 'Game over'
        messege_to_secreen(msg, RED, 'center', 'center', 'large')
        pygame.display.update()
        time.sleep(3)
        isGameStarted = False
        x = 0
        socketIO.emit('disconnect')



    def on_before_start_the_game(self):
        gameDisplay.fill(WHITE)

        if isGameStarted:
            messege_to_secreen('Waiting the other player to start the game', GREEN,'center', 'center', 'mid')
        else :
            messege_to_secreen('Press enter to start the game', GREEN,'bottom', 'center', 'mid')
            messege_to_secreen('Arcade Snake Game', GREEN,'center', 'center', 'large')



    def on_draw(self, *data):
        global x
        x += 1
        player = data[0]['player']
        food = data[0]['food']

        gameDisplay.fill(SELVER)

        for i in range(0, len(player)):
            for j in range(0, len(player[i]['body'])):
                pygame.draw.rect(gameDisplay, player[i]['color'], [player[i]['body'][j]['x'], player[i]['body'][j]['y'], player[i]['body'][j]['width'], player[i]['body'][j]['height']])

            if i == 0:
                messege_to_secreen('GREEN SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'left')
            elif(i == 1):
                messege_to_secreen('BLACK SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'right')
            else :
                messege_to_secreen('YELLOW SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'center')



        pygame.draw.rect(gameDisplay, food['color'], [food['rect']['x'], food['rect']['y'], food['rect']['width'], food['rect']['height']])




socketIO = SocketIO('localhost', 8080, Namespace)


def net():
    socketIO.define(Namespace, "/")

def on_starting():
    gameDisplay.fill(SELVER)
    messege_to_secreen('Redy..', GREEN,'center', 'center', 'large')
    pygame.display.update()
    time.sleep(5)
    gameDisplay.fill(SELVER)
    messege_to_secreen('GO!!', GREEN, 'center', 'center', 'large')
    pygame.display.update()
    time.sleep(1)

netThread = threading.Thread(target=net)
netThread.start()





while not gameExit:

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameExit = True

        elif event.type == pygame.KEYDOWN :

            if not isGameStarted:
                if event.key == pygame.K_RETURN:
                    isGameStarted = True
                    socketIO.emit('create new player')

                elif event.key == pygame.K_p :
                    isGameStarted = True

            else :
                if event.key == pygame.K_RIGHT :
                    socketIO.emit('changeDirction', 1)
                    pass;

                elif event.key == pygame.K_LEFT :
                    socketIO.emit('changeDirction', 2)
                    pass;
                elif event.key == pygame.K_UP :
                    socketIO.emit('changeDirction', 3)
                    pass;

                elif event.key == pygame.K_DOWN :
                    socketIO.emit('changeDirction', 4)
                    pass;


    socketIO.emit('draw request', isGameStarted)
    clock.tick(30)
    pygame.display.update()

    if x == 2 :
        messege_to_secreen('Redy!!', GREEN, 'center', 'center', 'large')
        pygame.display.update()
        time.sleep(2)
        gameDisplay.fill(SELVER)
        messege_to_secreen('GO!!', GREEN, 'center', 'center', 'large')
        pygame.display.update()
        time.sleep(0.24)
        x+=1


socketIO.emit('disconnect')
pygame.quit()
sys.exit()

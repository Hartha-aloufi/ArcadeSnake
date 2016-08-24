import pygame
from copy import deepcopy
import sys
from utility import *
from socketIO_client import SocketIO, BaseNamespace
import threading;



SELVER = (140, 140, 140)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


pygame.init()
gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hartha')
clock = pygame.time.Clock()



class Namespace(BaseNamespace):
    def on_server_emit(self, *args):
        print("received...")

    def on_connect(self):
        print("Connected")

    def on_draw(self, *data):
        player = data[0]['player']
        food = data[0]['food']

        gameDisplay.fill(SELVER)

        for i in range(0, len(player)):
            for j in range(0, len(player[i]['body'])):
                pygame.draw.rect(gameDisplay, player[i]['color'], [player[i]['body'][j]['x'], player[i]['body'][j]['y'], player[i]['body'][j]['width'], player[i]['body'][j]['height']])

        pygame.draw.rect(gameDisplay, food['color'], [food['rect']['x'], food['rect']['y'], food['rect']['width'], food['rect']['height']])
        pygame.display.update()



socketIO = SocketIO('localhost', 8080, Namespace)


def net():
    socketIO.define(Namespace, "/")


netThread = threading.Thread(target=net)
netThread.start();


gameExit = False




while not gameExit:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameExit = True

        elif event.type == pygame.KEYDOWN :

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

    socketIO.emit('draw request')
    clock.tick(15)


socketIO.emit('disconnect')
pygame.quit()
sys.exit()

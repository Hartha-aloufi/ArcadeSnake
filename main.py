import pygame
from copy import deepcopy
import sys
from utility import *

import threading;

# from flask import Flask;
# import socketio;


GREEN = (153, 204, 0)
YELLOW = (255, 191, 0)
SELVER = (140, 140, 140)
RED = (255, 0 , 0)
SNAKE_WIDTH = 12
SNAKE_HEIGHT = 12
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600






    


def net():
    from socketIO_client import SocketIO, BaseNamespace
    class Namespace(BaseNamespace):
        def on_server_emit(self, *args):
            print("received...");

        def on_connect(self):
            print("Connected");
    
    
    socketIO = SocketIO('localhost', 8080, Namespace)
    socketIO.define(Namespace, "/");


netThread = threading.Thread(target=net);
netThread.start();
    
pygame.init()


print("before");

print("after");
# socketIO.on('server_emit', Namespace.on_emit_server);

gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Hartha')


clock = pygame.time.Clock()



gameExit = False



def on_draw(self, *data):
    print('sdfsdfsdfsdf')
    print(data)
    for p in range(0, data.player):
        for rect in range(0, p.body):
            pygame.draw.rect(gameDisplay, p.color, [rect.x, rect.y, SNAKE_WIDTH, SNAKE_HEIGHT])

    pygame.draw.rect(gameDisplay, data.food.color, [data.food.rect.x, data.food.rect.y, data.food.rect.width, data.food.rect.height])
    gameDisplay.fill(SELVER)
    pygame.display.update()

def on_server_emit(*args):
    print("recieved from server")


## socketIO.on('draw', on_draw)
# Listen

while not gameExit:
    speed = 10
    ##socketIO.on('server_emit', on_server_emit)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            gameExit = True

        elif event.type == pygame.KEYDOWN :

            if event.key == pygame.K_RIGHT :
                ##socketIO.emit('changeDirction', 1)
                pass;

            elif event.key == pygame.K_LEFT :
                ##socketIO.emit('changeDirction', 2)
                pass;
            elif event.key == pygame.K_UP :
                ##socketIO.emit('changeDirction', 3)
                pass;

            elif event.key == pygame.K_DOWN :
                ##socketIO.emit('changeDirction', 4)
                pass;

    clock.tick(30)

##socketIO.off('server_emit')
pygame.quit()
sys.exit()

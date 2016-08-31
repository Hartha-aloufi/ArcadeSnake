import pygame
import sys
from utility import *
from socketIO_client import SocketIO, BaseNamespace
import threading
import time
import Queue

RASP = 0

if(RASP):
    import RPi.GPIO as GPIO


pygame.init()
display_info = pygame.display.Info()

SCREEN_WIDTH = display_info.current_w
SCREEN_HEIGHT = display_info.current_h - 64;

BLACK = (0,0,0)
GREEN = (153, 204, 0)
DARK_GREEN = (0, 255, 0)
WHITE = (255,255,255)
SELVER = (140, 140, 140)
RED = [255, 0 , 0]
DARK_RED = (177, 0, 0)
SNAKE_HEIGHT = h(13)
SNAKE_WIDTH = w(13)
#EYE_SIZE = 3
gameExit = False
isGameStarted = False
SPEED = 13

# threadQeue = Queue.Queue()

if RASP:
    GPIO.setmode(GPIO.BOARD);

# out1 = 31;
# out2 = 11;
# out3 = 35;
# out4 = 37;

in1 = 35;
in2 = 36
in3 = 37;
in4 = 38;


# GPIO.setup(out1, GPIO.OUT);
# GPIO.setup(out2, GPIO.OUT);
# GPIO.setup(out3, GPIO.OUT);
# GPIO.setup(out4, GPIO.OUT);

# GPIO.output(out1, True);
# GPIO.output(out2, True);
# GPIO.output(out3, True);
# GPIO.output(out4, True);

if RASP:
    # GPIO.setup(in1, GPIO.IN);
    GPIO.setup(in1, GPIO.IN, pull_up_down=GPIO.PUD_UP);
    # GPIO.setup(in2, GPIO.IN);
    GPIO.setup(in2, GPIO.IN, pull_up_down=GPIO.PUD_UP);
    # GPIO.setup(in3, GPIO.IN);
    GPIO.setup(in3, GPIO.IN, pull_up_down=GPIO.PUD_UP);
    # GPIO.setup(in4, GPIO.IN);
    GPIO.setup(in4, GPIO.IN, pull_up_down=GPIO.PUD_UP);






gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.NOFRAME)
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
    x,y =0,0

    if posV == 'top':
        x = h(20)
    elif posV == 'bottom' :
        x = SCREEN_HEIGHT - h(20)
    elif posV == 'center' :
        x = SCREEN_HEIGHT / 2

    if posH == 'right':
        y = w(50)
    elif posH == 'left':
        y = SCREEN_WIDTH - w(50)
    elif posH == 'center':
        y = SCREEN_WIDTH / 2

    textRect.center = y, x
    gameDisplay.blit(textSurf, textRect)

playMode = 1

def intro_menu():
    global playMode
    intro = True

    puse_mode_snake = Snake(BLACK, 0, SNAKE_WIDTH, SNAKE_HEIGHT, (w(50),h(50)), 1)
    puse_mode_food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, RED)

    while intro :

        gameDisplay.fill(WHITE)

        for event in pygame.event.get() :
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_LEFT :
                    playMode = 1
                elif event.key == pygame.K_RIGHT :
                    playMode = 2
                elif event.key == pygame.K_RETURN:
                    intro = False

        if playMode == 1 :
            pygame.draw.rect(gameDisplay, RED, [SCREEN_WIDTH /6, SCREEN_HEIGHT/1.5, SCREEN_WIDTH / 4, SCREEN_HEIGHT / 8])
        else :
            pygame.draw.rect(gameDisplay, DARK_RED, [SCREEN_WIDTH /6, SCREEN_HEIGHT/1.5,  SCREEN_WIDTH / 4, SCREEN_HEIGHT / 8])

        if playMode == 2 :
            pygame.draw.rect(gameDisplay, DARK_GREEN, [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.5,  SCREEN_WIDTH / 4, SCREEN_HEIGHT / 8])
        else :
            pygame.draw.rect(gameDisplay, GREEN, [SCREEN_WIDTH / 2,  SCREEN_HEIGHT / 1.5,  SCREEN_WIDTH / 4, SCREEN_HEIGHT / 8])

        textSurface = mid_font.render('Single player', True, WHITE)
        rect = textSurface.get_rect()
        rect.center = SCREEN_WIDTH / 6 + w(140), SCREEN_HEIGHT / 1.5 + h(46)

        gameDisplay.blit(textSurface, rect)

        textSurface = mid_font.render('Two players', True, WHITE)
        rect = textSurface.get_rect()
        rect.center = SCREEN_WIDTH / 2 + w(140), SCREEN_HEIGHT / 1.5 + h(46)

        gameDisplay.blit(textSurface, rect)

        messege_to_secreen('Arcade HACKATARI TEAM', GREEN,'center', 'center', 'large')


        puse_mode_snake.move(puse_mode_food, SCREEN_WIDTH, SCREEN_HEIGHT)
        puse_mode_snake.move_head(SPEED, SCREEN_WIDTH, SCREEN_HEIGHT)

        if puse_mode_snake.can_eat(puse_mode_food) :
            puse_mode_snake.eat()
            puse_mode_food.calc_new_pos()

            if puse_mode_snake.points == 50 :
                puse_mode_snake.re_init((w(20),h(20)))

        for i in range(0, len(puse_mode_snake.body)) :
            pygame.draw.rect(gameDisplay, puse_mode_snake.color, [puse_mode_snake.body[i].x, puse_mode_snake.body[i].y, SNAKE_WIDTH, SNAKE_HEIGHT])


        pygame.draw.rect(gameDisplay, GREEN, [puse_mode_snake.eyes[0].x, puse_mode_snake.eyes[0].y, puse_mode_snake.eyes[0].width, puse_mode_snake.eyes[0].height])
        pygame.draw.rect(gameDisplay, GREEN, [puse_mode_snake.eyes[1].x, puse_mode_snake.eyes[1].y, puse_mode_snake.eyes[1].width, puse_mode_snake.eyes[1].height])

        pygame.draw.rect(gameDisplay, puse_mode_food.color, [puse_mode_food.rect.x, puse_mode_food.rect.y, puse_mode_food.rect.width, puse_mode_food.rect.height])

        pygame.display.update()
        clock.tick(30)



intro_menu()



# single player
if playMode == 1 :
    player1_start_point = (w(20), h(20))
    hartha_start_point = (w(20), h(50))
    player1 = Snake(GREEN, 0, SNAKE_WIDTH, SNAKE_HEIGHT, player1_start_point, 1)
    hartha = Snake(BLACK, 0, SNAKE_WIDTH, SNAKE_HEIGHT, hartha_start_point, 1)

    food = Food(SCREEN_WIDTH, SCREEN_HEIGHT, RED)
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

                player1.update_snake_eyes()

        gameDisplay.fill(SELVER)

        if player1.move_head(SPEED, SCREEN_WIDTH, SCREEN_HEIGHT):
            if player1.detect_self_collision() :
                player1.color = RED
            else :
                player1.color = GREEN

        if player1.can_eat(food) :
            player1.eat()
            food.calc_new_pos()

        for i in range(0, len(player1.body)) :
            pygame.draw.rect(gameDisplay, player1.color, [player1.body[i].x, player1.body[i].y, SNAKE_WIDTH, SNAKE_HEIGHT])

        pygame.draw.rect(gameDisplay, BLACK, [player1.eyes[0].x, player1.eyes[0].y, player1.eyes[0].width, player1.eyes[0].height])
        pygame.draw.rect(gameDisplay, BLACK, [player1.eyes[1].x, player1.eyes[1].y, player1.eyes[1].width, player1.eyes[1].height])


        hartha.move(food, SCREEN_WIDTH, SCREEN_HEIGHT)
        hartha.move_head(SPEED, SCREEN_WIDTH, SCREEN_HEIGHT)

        if hartha.can_eat(food) :
            hartha.eat()
            food.calc_new_pos()

        for i in range(0, len(hartha.body)) :
            pygame.draw.rect(gameDisplay, hartha.color, [hartha.body[i].x, hartha.body[i].y, SNAKE_WIDTH, SNAKE_HEIGHT])


        pygame.draw.rect(gameDisplay, GREEN, [hartha.eyes[0].x, hartha.eyes[0].y, hartha.eyes[0].width, hartha.eyes[0].height])
        pygame.draw.rect(gameDisplay, GREEN, [hartha.eyes[1].x, hartha.eyes[1].y, hartha.eyes[1].width, hartha.eyes[1].height])

        pygame.draw.rect(gameDisplay, food.color, [food.rect.x, food.rect.y, food.rect.width, food.rect.height])



        messege_to_secreen('GREEN SNAKE : ' + (str(player1.points)), WHITE, 'bottom', 'left')
        messege_to_secreen('BLACK SNAKE : ' + (str(hartha.points)), WHITE, 'bottom', 'right')

        if player1.points == 20 or hartha.points == 20:
            if player1.points > hartha.points:
                messege_to_secreen('You win', GREEN, 'center', 'center', 'large')
            else :
                messege_to_secreen('Game over', RED, 'center', 'center', 'large')

            pygame.display.update()
            time.sleep(3)
            hartha.re_init(hartha_start_point)
            player1.re_init(player1_start_point)

            intro_menu()
        pygame.display.update()
        clock.tick(30)

    if  gameExit :
        pygame.quit()
        sys.exit()

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
            messege_to_secreen('Arcade HACKATARI TEAM', GREEN,'center', 'center', 'large')



    def on_draw(self, *data):
        # threadQeue.put(data)
        print('co')
        global x
        x += 1
        player1 = data[0]['player1']
        player2 = data[0]['player2']
        player1Dir = data[0]['player1Dir']
        player2Dir = data[0]['player2Dir']
        player1Points = data[0]['player1Points']
        player2Points = data[0]['player2Points']
        player1Col = data[0]['player1Col']
        player2Col = data[0]['player2Col']
        food = data[0]['food']

        gameDisplay.fill(SELVER)

        # new Rectangle(this.body[0].x + width - 5, this.body[0].y + height - 10), new Rectangle(this.body[0].x + width - 5, this.body[0].y + height - 5)
        global GREEN, BLACK

        if player1Col :
            GREEN = RED
        i = 0
        while(i < len(player1)-1):
            pygame.draw.rect(gameDisplay, GREEN, [player1[i], player1[i+1], 13,13])
            i = i + 2

        GREEN = (153, 204, 0)

        if player1Dir == 1 :
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 5, player1[1] + SNAKE_HEIGHT - 10, 3, 3])
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 5, player1[1] + SNAKE_HEIGHT - 5, 3, 3])

        elif player1Dir == 2 :
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 10, player1[1] + SNAKE_HEIGHT - 10, 3, 3])
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 10, player1[1] + SNAKE_HEIGHT - 5, 3, 3])

        elif player1Dir == 3 :
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 10, player1[1] + SNAKE_HEIGHT - 10, 3, 3])
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 5, player1[1] + SNAKE_HEIGHT - 10, 3, 3])

        elif player1Dir == 4 :
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 10, player1[1] + SNAKE_HEIGHT - 5, 3, 3])
            pygame.draw.rect(gameDisplay, BLACK, [player1[0] + SNAKE_WIDTH - 5, player1[1] + SNAKE_HEIGHT - 5, 3, 3])


        if player2Col :
            BLACK = RED

        i = 0
        while(i < len(player2) - 1) :
            pygame.draw.rect(gameDisplay, BLACK, [player2[i], player2[i+1], 13,13])
            i = i + 2

        BLACK = (0,0,0)

        if player2Dir == 1 :
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 5, player2[1] + SNAKE_HEIGHT - 10, 3, 3])
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 5, player2[1] + SNAKE_HEIGHT - 5, 3, 3])

        elif player2Dir == 2 :
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 10, player2[1] + SNAKE_HEIGHT - 10, 3, 3])
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 10, player2[1] + SNAKE_HEIGHT - 5, 3, 3])

        elif player2Dir == 3 :
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 10, player2[1] + SNAKE_HEIGHT - 10, 3, 3])
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 5, player2[1] + SNAKE_HEIGHT - 10, 3, 3])

        elif player2Dir == 4 :
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 10, player2[1] + SNAKE_HEIGHT - 5, 3, 3])
            pygame.draw.rect(gameDisplay, GREEN, [player2[0] + SNAKE_WIDTH - 5, player2[1] + SNAKE_HEIGHT - 5, 3, 3])


        pygame.draw.rect(gameDisplay, RED, [food[0], food[1], 7,7])

        messege_to_secreen('GREEN SNAKE : ' + (str(player1Points)), WHITE, 'bottom', 'left')
        messege_to_secreen('BLACK SNAKE : ' + (str(player2Points)), WHITE, 'bottom', 'right')
        # for i in range(0, len(player)):
        #     for j in range(0, len(player[i]['body'])):
        #         pygame.draw.rect(gameDisplay, player[i]['color'], [player[i]['body'][j]['x'], player[i]['body'][j]['y'], player[i]['body'][j]['width'], player[i]['body'][j]['height']])
        #
        #     if i == 0:
        #         messege_to_secreen('GREEN SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'left')
        #     elif(i == 1):
        #         messege_to_secreen('BLACK SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'right')
        #     else :
        #         messege_to_secreen('YELLOW SNAKE : ' + (str(player[i]['points])), WHITE, 'bottom', 'center')



        # pygame.draw.rect(gameDisplay, food['color'], [food['rect']['x'], food['rect']['y'], food['rect']['width'], food['rect']['height']])




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


state = 1;
try:
    while not gameExit:
        # input = GPIO.input(in1);
        # print(GPIO.input(in1));
        # if input:
        #     print("INNNNNNPUT");

        if RASP:

            if not GPIO.input(in1) and not state == 1:
                socketIO.emit('changeDirction', 1)
                state = 1;
                pass;

            elif not GPIO.input(in2) and not state == 2:
                socketIO.emit('changeDirction', 2)
                state = 2;
                pass;

            elif not GPIO.input(in3) and not state == 3:
                socketIO.emit('changeDirction', 3);
                state = 3;
                pass;

            elif not GPIO.input(in4) and not state == 4:
                socketIO.emit('changeDirction', 4)
                state = 4;
                pass;

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                gameExit = True

            elif event.type == pygame.KEYDOWN :

                if not isGameStarted:
                    if event.key == pygame.K_RETURN:
                        isGameStarted = True
                        socketIO.emit('create new player', SCREEN_WIDTH, SCREEN_HEIGHT)

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
        clock.tick(10)

        pygame.display.update()

        if x == 2 :
            messege_to_secreen('Ready!!', GREEN, 'center', 'center', 'large')
            pygame.display.update()
            time.sleep(2)
            gameDisplay.fill(SELVER)
            messege_to_secreen('GO!!', GREEN, 'center', 'center', 'large')
            pygame.display.update()
            time.sleep(0.24)
            x+=1

except KeyboardInterrupt:
    print("cleaning up");
    if RASP:
        GPIO.cleanup();

socketIO.emit('disconnect')

socketIO.emit('disconnect')
pygame.quit()
sys.exit()

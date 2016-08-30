
class SnakeMultiplayer :

SCREEN_WIDTH = display_info.current_w - 80
SCREEN_HEIGHT = display_info.current_h - 20

BLACK = (0,0,0)
GREEN = (153, 204, 0)
DARK_GREEN = (0, 255, 0)
WHITE = (255,255,255)
SELVER = (140, 140, 140)
RED = [255, 0 , 0]
DARK_RED = (177, 0, 0)
SNAKE_HEIGHT = 13
SNAKE_WIDTH = 13
EYE_SIZE = 3
gameExit = False
isGameStarted = False

threadQeue = Queue.Queue()

# 
# gameDisplay = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.NOFRAME)
# pygame.display.set_caption('Snake')
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
    foodColorCnt = 0
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
            global GREEN, BLACK, foodColorCnt

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

            foodColorCnt = foodColorCnt % 21

            if foodColorCnt <= 10 :
                pygame.draw.rect(gameDisplay, RED, [food[0], food[1], 18,18])
            elif foodColorCnt <= 20 :
                pygame.draw.rect(gameDisplay, (255,255,0), [food[0], food[1], 18,18])


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
            #         messege_to_secreen('YELLOW SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'center')



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
    #
    # netThread = threading.Thread(target=net)
    # netThread.start()





    def run() :
        while not gameExit:

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

            # if not threadQeue.empty():
            #     data = threadQeue.get()
            #
            #     global x
            #     x += 1
            #     player = data[0]['player']
            #     food = data[0]['food']
            #
            #     gameDisplay.fill(SELVER)
            #
            #     for i in range(0, len(player)):
            #         for j in range(0, len(player[i]['body'])):
            #             pygame.draw.rect(gameDisplay, player[i]['color'], [player[i]['body'][j]['x'], player[i]['body'][j]['y'], player[i]['body'][j]['width'], player[i]['body'][j]['height']])
            #
            #         if i == 0:
            #             messege_to_secreen('GREEN SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'left')
            #         elif(i == 1):
            #             messege_to_secreen('BLACK SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'right')
            #         else :
            #             messege_to_secreen('YELLOW SNAKE : ' + (str(player[i]['points'])), WHITE, 'bottom', 'center')
            #
            #
            #
            #     pygame.draw.rect(gameDisplay, food['color'], [food['rect']['x'], food['rect']['y'], food['rect']['width'], food['rect']['height']])

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


    socketIO.emit('disconnect')

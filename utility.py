from random import randint




class ConstsC:

    def __init__(self):
        self.screenWidth = 1280;
        self.screenHeight = 800;
        self.constWidth = 1280;
        self.constHeight = 800;


Consts = ConstsC();


def w(x):
    return (x * (Consts.screenWidth/Consts.constWidth));

def h(y):
    return (y * (Consts.screenHeight/Consts.constHeight));



class Snake:
    # body[0] is the snake head

    def __init__(self, color, points, width, height, start_point, direc):
        self.body = [Rectangle(start_point[0], start_point[1], width, height)]
        self.color = color
        self.points = points
        self.direc = direc
        self.eyes = [Rectangle(self.body[0].x + width/1.25, self.body[0].y + height/2.5, 3, 3),Rectangle(self.body[0].x + width/1.25, self.body[0].y + height/1.25, 3, 3)]
        self.error_x = 0
        self.error_y = 0
        self.error_handler = 0
        self.vFood = [Food(1000,1000,(0,0,0)), Food(1000,1000,(0,0,0)), Food(1000,1000,(0,0,0))]
        self.error_frames = 0

    def re_init(self, start_point) :
        self.points = 0
        self.body = [Rectangle(start_point[0], start_point[1], self.body[0].width, self.body[0].height)]

    def can_eat(self, food) :
        # collision detection
        if self.body[0].x < food.rect.x + food.rect.width and  self.body[0].x + self.body[0].width > food.rect.x and self.body[0].y < food.rect.y + food.rect.height and self.body[0].height + self.body[0].y > food.rect.y :
            return True

        return False



    def eat(self):
        self.points += 1
        self.body.append(Rectangle(self.body[0].x, self.body[0].y, self.body[0].width, self.body[0].height))
        self.error_handler += 1



    def move_head(self, speed, width, height):
        new_x = self.body[0].x
        new_y = self.body[0].y

        if self.direc == 1 :
            new_x += w(speed)
            new_x %= width

        elif self.direc == 2 :
            new_x -= w(speed)
            new_x %= width

        elif self.direc == 3 :
            new_y -= h(speed)
            new_y %= height

        elif self.direc == 4 :
            new_y += h(speed)
            new_y %= height

        if new_x < width and new_x > -1 and new_y < height and new_y > -1 :
            tempx = self.body[0].x
            tempy = self.body[0].y

            self.move_body()
            self.body[0].y = new_y
            self.body[0].x = new_x
            self.update_snake_eyes()

        return True


    def move_body(self):
        length = len(self.body)

        for i in range(1, len(self.body)) :
            self.body[length - i].x = self.body[length - i - 1].x
            self.body[length - i].y = self.body[length - i - 1].y


    def detect_collision_with_other_player(self, other):
        for i in range(1, len(other.body)) :
            if self.body[0].x < other.body[i].x + other.body[i].width and  self.body[0].x + self.body[0].width > other.body[i].x and self.body[0].y < other.body[i].y + other.body[i].height and self.body[0].height + self.body[0].y > other.body[i].y :
                return True

    def detect_self_collision(self):
        for i in range(3, len(self.body)):
            if self.body[0].x < self.body[i].x + self.body[i].width and  self.body[0].x + self.body[0].width > self.body[i].x and self.body[0].y < self.body[i].y + self.body[i].height and self.body[0].height + self.body[0].y > self.body[i].y :
                return True

        return False

    def update_snake_eyes(self):
        if self.direc == 1:
            self.eyes = [Rectangle(self.body[0].x + self.body[0].width / 1.62, self.body[0].y + self.body[0].height / 4.3, 3, 3),
                        Rectangle(self.body[0].x + self.body[0].width / 1.62 , self.body[0].y + self.body[0].height / 1.62, 3, 3)]

        elif self.direc == 2 :
            self.eyes = [Rectangle(self.body[0].x + self.body[0].width / 4.3, self.body[0].y + self.body[0].height / 4.3, 3, 3),
                        Rectangle(self.body[0].x + self.body[0].width / 4.3 , self.body[0].y + self.body[0].height / 1.62, 3, 3)]


        elif self.direc == 3 :
            self.eyes = [Rectangle(self.body[0].x + self.body[0].width / 4.3, self.body[0].y + self.body[0].height / 4.3, 3, 3),
                        Rectangle(self.body[0].x + self.body[0].width / 1.62 , self.body[0].y + self.body[0].height / 4.3, 3, 3)]

        else :
            self.eyes = [Rectangle(self.body[0].x + self.body[0].width / 1.62, self.body[0].y + self.body[0].height / 1.62, 3, 3),
                        Rectangle(self.body[0].x + self.body[0].width / 4.3 , self.body[0].y + self.body[0].height / 1.62, 3, 3)]


    def create_random_food(self, number_of_food, orig_food, screen_width, screen_height):
        for i in range(0, number_of_food) :
            self.vFood[i].rect.x = (orig_food.rect.x + randint(w(-200), w(200)) % screen_width + screen_width) % screen_width
            self.vFood[i].rect.y = (orig_food.rect.y + randint(h(-200), h(200)) % screen_height + screen_height) % screen_height

            self.vFood[i].rect.x = max(self.vFood[i].rect.x, w(20))
            self.vFood[i].rect.y = max(self.vFood[i].rect.y, h(20))
    # AI
    def move(self, food, screen_width, screen_height):
        self.error_frames += 1

        if self.error_handler == 0 :
            self.food_to_eat = food
            self.create_random_food(3, food, screen_width, screen_height)
        elif self.error_handler < 3:
            self.food_to_eat = self.vFood[self.error_handler]

            if self.can_eat(self.food_to_eat) :
                self.error_handler += 1
                self.error_frames = 0
        else :
            self.error_handler = 0


        if self.error_frames == 200 :
            self.create_random_food(3, food, screen_width, screen_height)
            self.direc = randint(1, 4)
            self.error_frames = 0

        # self.error_handler += 1
        #
        # if self.error_handler == 50:
        #     self.error_x = randint(-200,200)
        #     self.error_y = randint(-200,200)
        #     self.error_handler = 0
        #     self.vFood.rect.x = food.rect.x + self.error_x
        #     self.vFood.rect.y = food.rect.y + self.error_y
        #
        # elif self.can_eat(self.vFood) :
        #     self.error_y = 0
        #     self.error_x = 0

        if self.food_to_eat.rect.x - self.body[0].x > self.body[0].width :
            if self.direc == 2 :
                self.direc = 3
            else :
                self.direc = 1

        elif self.food_to_eat.rect.x - self.body[0].x < -self.body[0].width :
            if self.direc == 1:
                self.direc = 4
            else:
                self.direc = 2

        elif self.food_to_eat.rect.y - self.body[0].y > self.body[0].height :
            if self.direc == 3:
                self.direc = 1
            else:
                self.direc = 4

        elif self.food_to_eat.rect.y - self.body[0].y < -self.body[0].height:
            if self.direc == 4:
                self.direc = 2
            else:
                self.direc = 3


        # self.error_handler += 1
        #
        # if self.error_handler == 10 :
        #     random_numer = randint(0, 20)
        #
        #     if random_numer % 2 == 0:
        #         self.direc = randint(1, 4)


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class Food:

    def __init__(self, screen_width, screen_height, color):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.color = color
        self.rect = Rectangle(0,0,w(7),h(7))
        self.calc_new_pos()

    def calc_new_pos(self):
        self.rect.x = randint(0, self.screen_width-w(20))
        self.rect.y = randint(0, self.screen_height-h(20))

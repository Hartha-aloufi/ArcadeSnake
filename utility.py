from random import randint


class Snake:
    # body[0] is the snake head

    def __init__(self, color, points, width, height, start_point, direc):
        self.body = [Rectangle(start_point[0], start_point[1], width, height)]
        self.color = color
        self.points = points
        self.direc = direc


    def can_eat(self, food) :
        # collision detection
        if self.body[0].x < food.rect.x + food.rect.width and  self.body[0].x + self.body[0].width > food.rect.x and self.body[0].y < food.rect.y + food.rect.height and self.body[0].height + self.body[0].y > food.rect.y :
            return True

        return False



    def eat(self):
        self.points += 1
        self.body.append(Rectangle(self.body[0].x, self.body[0].y, self.body[0].width, self.body[0].height))



    def move_head(self, speed, width, height):
        new_x = self.body[0].x
        new_y = self.body[0].y

        if self.direc == 1 :
            new_x += speed
        elif self.direc == 2 :
            new_x -= speed
        elif self.direc == 3 :
            new_y -= speed
        elif self.direc == 4 :
            new_y += speed

        if new_x < width and new_x > -1 and new_y < height and new_y > -1 :
            self.move_body()
            self.body[0].x = new_x
            self.body[0].y = new_y


    def move_body(self):
        length = len(self.body)

        for i in range(1, len(self.body)) :
            self.body[length - i].x = self.body[length - i - 1].x
            self.body[length - i].y = self.body[length - i - 1].y


    def detect_self_collision(self):
        for i in range(3, len(self.body)):
            if self.body[0].x < self.body[i].x + self.body[i].width and  self.body[0].x + self.body[0].width > self.body[i].x and self.body[0].y < self.body[i].y + self.body[i].height and self.body[0].height + self.body[0].y > self.body[i].y :
                return True

        return False


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
        self.rect = Rectangle(0,0,7,7)
        self.calc_new_pos()

    def calc_new_pos(self):
        self.rect.x = randint(0, self.screen_width-20)
        self.rect.y = randint(0, self.screen_height-20)

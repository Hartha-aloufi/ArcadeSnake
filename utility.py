class Snake:
    def __init__(self, color, points, width, height, start_point, direc):
        self.body = [rectangle(start_point[0], start_point[1])]
        self.color = color
        self.points = points
        self.width = width
        self.height = height
        self.direc = direc

    def eat(self):
        self.points += 1
        self.body.append(rectangle(start_point[0], start_point[1]))



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
        for i in range(1, len(self.body)) :
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y


class rectangle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

from Rectangle import Rectangle;
from utility import *;
from random import randint;
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

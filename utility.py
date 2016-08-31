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









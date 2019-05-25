import random
from pygame.sprite import Sprite
from item import Item

class Fruit(Sprite):
    def __init__(self, game, rate = 1, pos_x = None, pos_y = None, mode = 0):
        Sprite.__init__(self)
        self.game = game
        self.rate = rate
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.load()
        self.set_path()


    def load(self):
        self.img = self.game.imgs['f' + str(random.randint(1, 15))]
        self.rect = self.img.get_rect()


    def set_path(self):
        self.rect.x = random.randint(int(-self.game.screen_width/5), int(self.game.screen_width/5) * 6) if self.pos_x == None else self.pos_x
        self.rect.y = int(self.game.screen_height * 1.05) if self.pos_y == None else self.pos_y
        self.speed_x = self.game.screen_width/2000 * random.uniform(8, 12) * random.choice([-1, 1])
        self.speed_y = (-1) * self.game.screen_height/250 * random.uniform(3, 8)
        self.g = self.game.screen_height/4000

    def update(self):
        self.rect.x += self.speed_x * self.rate
        self.rect.y += self.speed_y * self.rate
        self.speed_y += self.g * self.rate
        self.game.screen.blit(self.img, self.rect)
        if ((self.rect.x <= int(-self.game.screen_width/5) and self.speed_x < 0) 
            or (self.rect.x >= int(self.game.screen_width/5) * 6 and self.speed_x > 0)
            or (self.rect.y <= int(-self.game.screen_height/5) and self.speed_y > 0 )):
            self.reset()

    def reset(self):
        self.set_path()



class Clock(Fruit):
    def __init__(self, game, rate = 1, pos_x = None, pos_y = None, mode = 0):
        Fruit.__init__(self, game, rate, pos_x, pos_y, mode)

    def load(self):
        self.img = self.game.imgs['ft']
        self.rect = self.img.get_rect()

class Frog(Fruit):
    def __init__(self, game, rate = 1, pos_x = None, pos_y = None, mode = 0):
        Fruit.__init__(self, game, rate, pos_x, pos_y, mode)

    def load(self):
        self.img = self.game.imgs['ff']
        self.rect = self.img.get_rect()
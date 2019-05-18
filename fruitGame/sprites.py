import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import cv2
import numpy as np
import sys
import random
import setting

from item import Item

class Fruits(Sprite):
    def __init__(self,choose_fruit,screen,w,h):
        Sprite.__init__(self)
        self.screen = screen
        self.image = choose_fruit
        self.rect = self.image.get_rect()
        self.item = Item(w, h, rate = 9,mode=0)#5-
    def set_xy(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def load(self):
        self.screen.blit(pygame.transform.scale(self.image,(300,300)),self.rect)
    def update(self):
        (self.rect.x, self.rect.y) = self.item.refresh()

class Clock(Sprite):
    def __init__(self,get_clock,screen,w,h):
        Sprite.__init__(self)
        self.screen = screen
        self.image = get_clock
        self.rect = self.image.get_rect()
        self.item = Item(w, h, rate = 9,mode=0)#5-
    def set_xy(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def load(self):
        self.screen.blit(pygame.transform.scale(self.image,(300,300)),self.rect)
    def update(self):
        (self.rect.x, self.rect.y) = self.item.refresh()

class Frog(Sprite):
    def __init__(self,get_frog,screen,w,h):
        Sprite.__init__(self)
        self.screen = screen
        self.image = get_frog
        self.rect = self.image.get_rect()
        self.item = Item(w, h, rate = 9,mode=0)#5-
    def set_xy(self,x,y):
        self.rect.x = x
        self.rect.y = y
    def load(self):
        self.screen.blit(pygame.transform.scale(self.image,(300,300)),self.rect)
    def update(self):
        (self.rect.x, self.rect.y) = self.item.refresh()

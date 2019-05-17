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
        get_setting = setting.Setting()
        self.screen = screen
        self.image = choose_fruit
        self.rect = self.image.get_rect()
        self.item = Item(w, h, rate = 9,mode=0)#5-
        # self.x_speed = x_speed
        # self.y_speed = y_speed
        # self.x_acceleration = x_acceleration
        # self.y_acceleration = y_acceleration
    def set_xy(self,x,y):
        self.rect.x = x
        self.rect.y = y

    def load(self):
        self.screen.blit(pygame.transform.scale(self.image,(300,300)),self.rect)
        # print(self.rect.width)
        # print(self.rect.height)
    def update(self):
        (self.rect.x, self.rect.y) = self.item.refresh()
        # print('x:')
        # print(self.rect.x)
        # print('y:')
        # print(self.rect.y)
        #(self.rect.x, self.rect.y) = (500,500)


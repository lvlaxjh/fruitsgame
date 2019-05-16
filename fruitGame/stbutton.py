import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import cv2
import numpy as np
import sys
import random
import setting
from img_percess import percess
from item import Item

class StButton(Sprite):
    def __init__(self,choose_bt,screen):
        Sprite.__init__(self)
        self.get_setting = setting.Setting()
        self.screen = screen
        self.image = choose_bt
        self.tran_img = pygame.transform.scale(self.image,setting.Setting().start_game_img)
        self.rect = self.image.get_rect()
        self.angle = 0
    def set_xy(self,xy):
        self.rect.x = xy[0]
        self.rect.y = xy[1]

    def load(self):
        self.screen.blit(self.tran_img,self.rect)
    def update(self):
        self.angle += 1
        if self.angle>360:
            self.angle = 0
        self.tran_img=pygame.transform.rotate(self.tran_img,self.angle)
        #(self.rect.x, self.rect.y) = (500,500)


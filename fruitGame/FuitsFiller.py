import pygame
import threading
import sys
import cv2
import time
import numpy as np
from img_percess_red import percess_by_hsv
from pygame.sprite import Group, Sprite
from pygame.locals import *
from MySprite import *

class mouseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    
    def get_pos(self):
        return self.pos

    def start(self):
        while True:
            self.pos = pygame.mouse.get_pos()
            print(self.pos)

class Game():
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.init_settings()
        self.init_source()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        
        pygame.display.set_caption("Fruits Killer")
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.fruit_group = Group()
        self.clock_group = Group()
        self.frog_group = Group()

        #self.mouse = mouseThread()
        self.mouse = pygame.mouse

        self.font = pygame.font.SysFont('宋体', 100)
        self.timeboard_pos = (0, 0)
        self.scoreboard_pos = (0, 60)
        self.game_status = 'menu'
        self.button_status = str()

    def init_source(self):
        pygame.mixer.music.load('music/幼女幻奏.mp3')
        self.imgs = {
            'f1': pygame.image.load('img/fruit/f1.png'),
            'f2': pygame.image.load('img/fruit/f2.png'),
            'f3': pygame.image.load('img/fruit/f3.png'),
            'f4': pygame.image.load('img/fruit/f4.png'),
            'f5': pygame.image.load('img/fruit/f5.png'),
            'f6': pygame.image.load('img/fruit/f6.png'),
            'f7': pygame.image.load('img/fruit/f7.png'),
            'f8': pygame.image.load('img/fruit/f8.png'),
            'f9': pygame.image.load('img/fruit/f9.png'),
            'f10': pygame.image.load('img/fruit/f10.png'),
            'f11': pygame.image.load('img/fruit/f11.png'),
            'f12': pygame.image.load('img/fruit/f12.png'),
            'f13': pygame.image.load('img/fruit/f13.png'),
            'f14': pygame.image.load('img/fruit/f14.png'),
            'f15': pygame.image.load('img/fruit/f15.png'),
            'ff': pygame.image.load('img/fruit/ff.png'),
            'ft': pygame.image.load('img/fruit/t.png'),
        }
        self.menu_imgs = {
            'background': pygame.image.load('img/start/bk.jpg'),
            'start': pygame.image.load('img/start/start.png'),
            'option': pygame.image.load('img/start/option.png'),
            'exit': pygame.image.load('img/start/exit.png')
        }
        self.menu_rect = dict()
        for key, value in self.imgs.items():
            self.imgs[key] = pygame.transform.scale(value, self.fruit_size)
        for key, value in self.menu_imgs.copy().items():
            self.menu_imgs[key] = pygame.transform.scale(self.menu_imgs[key], self.menu_rect_size[key])
            self.menu_imgs[key + '_focus'] = pygame.transform.scale(self.menu_imgs[key], self.menu_rect_size[key + '_focus'])
        for key, value in self.menu_imgs.items():
            self.menu_rect[key] = value.get_rect()
            self.menu_rect[key].topleft = self.menu_rect_pos[key]

    def init_settings(self):
        self.screen_width = 1280
        self.screen_height = 720
        self.button_rate = 1.2
        self.fruit_size = (150, 150)
        self.clock_size = (150, 150)
        self.frog_size = (150, 150)
        self.fruit_count = 20
        self.clock_count = 3
        self.frog_count = 2
        self.countdown = 30
        self.score_per_fruit = 100
        self.score = 0
        self.menu_rect_size = {
            'background': (self.screen_width, self.screen_height),
            'start':(160, 160),
            'option':(160, 160),
            'exit':(160, 160)
        }
        self.menu_rect_pos = {
            'background': (0, 0),
            'start':(100, 400),
            'option':(500, 400),
            'exit':(900, 400),
        }
        self.button_game_mapping = {
            'start': 'game',
            'option': 'menu',
            'exit': 'exit'
        }
        for key, value in self.menu_rect_size.copy().items():
            self.menu_rect_size[key + '_focus'] = (int(value[0] * self.button_rate), int(value[1] * self.button_rate))
        for key, value in self.menu_rect_pos.copy().items():
            self.menu_rect_pos[key + '_focus'] = value

    def draw_cursor(self, pos):
        pygame.draw.circle(self.screen, [0, 255, 0], pos, 10)

    
    def cursor_in_rect(self, rect, pos):
        if pos[0] >= rect.left and pos[0] <= rect.right and pos[1] <= rect.bottom and pos[1] >= rect.top:
            return 1
        else:
            return 0

    def mouse_is_down(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                return 1
        return 0


    def cursor_in_button(self, button):
        if self.cursor_in_rect(self.menu_rect[button], pos = self.pos):
            self.screen.blit(self.menu_imgs[button + '_focus'], self.menu_rect[button + '_focus'])
            self.button_status = button
        else:
            self.screen.blit(self.menu_imgs[button], self.menu_rect[button])


    def refresh_menu(self):
        self.pos = self.mouse.get_pos()
        self.screen.blit(self.menu_imgs['background'], self.menu_rect['background'])
        self.cursor_in_button('start')
        self.cursor_in_button('option')
        self.cursor_in_button('exit')
        if self.mouse_is_down() and self.button_status is not None:
            self.game_status = self.button_game_mapping[self.button_status]
            if self.game_status =='game':
                self.init_sprites()
                self.start_time = time.time()
        self.button_status = None


    def init_sprites(self):
        for i in range(self.fruit_count):
            fruit = Fruit(self)
            self.fruit_group.add(fruit)
        for i in range(self.clock_count):
            clock = Clock(self)
            self.clock_group.add(clock)
        for i in range(self.frog_count):
            frog = Frog(self)
            self.frog_group.add(frog)
        


    def refresh_game(self):
        ret, frame = self.cap.read()
        #self.pos = percess_by_hsv(frame)
        self.pos = self.mouse.get_pos()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        self.screen.blit(frame, (0, 0))
        for fruit in self.fruit_group.sprites():
            if self.cursor_in_rect(fruit.rect, pos = self.pos):
                self.score += self.score_per_fruit
                fruit.reset()
            fruit.update()
        for frog in self.frog_group.sprites():
            if self.cursor_in_rect(frog.rect, pos = self.pos):
                self.countdown -= 5
                frog.reset()
            frog.update()
        for clock in self.clock_group.sprites():
            if self.cursor_in_rect(clock.rect, pos = self.pos):
                self.countdown += 5
                clock.reset()
            clock.update()
        time_seen = self.countdown - int(time.time() - self.start_time)
        scoreboard = self.font.render('SCORE: ' + str(self.score), 1, (255, 0, 0))
        timeboard = self.font.render('TIME: ' + str(time_seen), 1, (255, 0, 0))
        self.screen.blit(scoreboard, self.scoreboard_pos)
        self.screen.blit(timeboard, self.timeboard_pos)
        if time_seen == 0:
            self.game_status = 'exit'

    def start(self):
        while True:
            if pygame.mixer.music.get_busy() == False:
                pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == QUIT: # 点击右上角的'X'，终止主循环
                    pygame.quit()
                    sys.exit()       
                elif event.type == KEYDOWN:           
                    if event.key == K_ESCAPE: # 按下'ESC'键，终止主循环
                        pygame.quit()
                        sys.exit()   
            

            self.clock.tick(30)

            if self.game_status == 'menu':
                self.refresh_menu()
            elif self.game_status == 'game':
                self.refresh_game()
            elif self.game_status == 'exit':
                pygame.quit()
                sys.exit(0)

            self.draw_cursor(self.pos)

            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.start()

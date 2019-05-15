import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import cv2
import numpy as np
import sys
import random
import setting 
from img_percess import percess
from fruit import Fruits
get_all_img ={
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
    't': pygame.image.load('img/fruit/t.png'),
    'st_bk':pygame.image.load('img/start/bk.jpg'),
}
#设置
game_setting = setting.Setting()
#随机选取水果
def get_fruit():
    get_num = random.randint(1,15)
    fruit_one = str('img/fruit/f')+str(get_num)+str('.png')
    #fruit_one = 'img/fruit/t.png'
    return fruit_one
#cv转pygame用
def cvimage_to_pygame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame
#界面更新
def update_screen(screen,fruits_group,mouse_xy):
    screen.fill((0, 0, 0))  # 测试使用,使用调用frame摄像头

    pygame.draw.circle(screen, [255, 0, 0], mouse_xy, 5)

    for i in fruits_group.sprites():
        i.load()
    pygame.display.flip()
    
#界面事件
def update_event(screen,fruits_group,mouse_xy):
    for fruit_one in all_fruit_group:
        if mouse_xy[0]> fruit_one.rect.x+30 and mouse_xy[0] < fruit_one.rect.x+fruit_one.rect.width-30:
            if mouse_xy[1]>fruit_one.rect.y+30 and mouse_xy[1]<fruit_one.rect.y +fruit_one.rect.height-30:
                all_fruit_group.remove(fruit_one)

        if fruit_one.rect.y > game_setting.screen_height+400 or fruit_one.rect.x<-400 or fruit_one.rect.x>game_setting.screen_width+400:
            all_fruit_group.remove(fruit_one)
    if len(fruits_group) < 5:
        create_fruit = Fruits(get_fruit(),screen,game_setting.screen_width,game_setting.screen_height)
        create_fruit.set_xy(-50, 900)
        fruits_group.add(create_fruit)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
def start_interface_screen(start_all_img,screen,mouse_xy):
    #screen.fill((0, 0, 0))
    #背景
    # screen.fill(pygame.image.load('img/start/bk.png').convert())
    screen.blit(get_all_img['st_bk'],(0,0))
    #开始游戏按钮
    # screen.blit(start_all_img['start_game'],(30,600))
    # #设置按钮
    # screen.blit(start_all_img['setting_game'],(400,500))
    # #退出按钮
    # screen.blit(start_all_img['esc_game'],(800,300))
    pygame.draw.circle(screen, [255, 0, 0], mouse_xy, 5)
    #pygame.display.update(screen.blit(start_all_img['esc_game'],(800,300)))
    pygame.display.flip()
def start_interface_event(start_all_img,screen,mouse_xy):

    # start_all_img['start_game']=pygame.transform.rotate(start_all_img['start_game'] , 89)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

if __name__ == "__main__":
    #pygame初始化
    pygame.init()
    #界面初始化
    screen = pygame.display.set_caption('fuck fruits')
    screen = pygame.display.set_mode((game_setting.screen_width,game_setting.screen_height),pygame.FULLSCREEN|pygame.HWSURFACE)
    clock = pygame.time.Clock()
    #创建水果
    all_fruit_group = Group()
    #开始界面使用的图片
    start_all_img = {
        'start_game':pygame.transform.scale(pygame.image.load(get_fruit()),game_setting.start_game_img),
        'setting_game':pygame.transform.scale(pygame.image.load(get_fruit()),game_setting.setting_game_img),
        'esc_game':pygame.transform.scale(pygame.image.load(get_fruit()),game_setting.esc_game_img),
    }
    screen.blit(pygame.image.load('img/start/bk.png').convert(),(0,0))
    mouse=pygame.mouse
    while True:
        clock.tick(30)
        #mouse
        mouse_xy = mouse.get_pos()
        update_event(screen,all_fruit_group,mouse_xy)
        all_fruit_group.update()
        update_screen(screen,all_fruit_group,mouse_xy)
        # start_interface_screen(start_all_img,screen,mouse_xy)
        # start_interface_event(start_all_img,screen,mouse_xy)


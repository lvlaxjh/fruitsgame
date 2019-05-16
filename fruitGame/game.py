import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import cv2
import numpy as np
import sys
import random
import threading
#
import setting
from img_percess import percess
from fruit import Fruits
from stbutton import StButton
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
    'st_st':pygame.image.load('img/start/st.png'),
    'st_op':pygame.image.load('img/start/op.png'),
    'st_ex':pygame.image.load('img/start/ex.png'),
}
#设置
game_setting = setting.Setting()
st_bt_is_on = [0,0,0]#开始界面按钮的逻辑
'''
control_game:
    0-初始界面
    1-校准界面(判定红色)
    2-游戏界面
    3-设置界面
    4-退出

'''
control_game = 0
#进入不同界面的逻辑
#鼠标线程
class mouse_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mouse_xy = (0,0)
    def run(self):
        while True:
            self.mouse_xy = pygame.mouse.get_pos()
            # print(self.mouse_xy)

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
def start_interface_screen(screen,start_button_dict,mouse_xy):
    #screen.fill((0, 0, 0))
    #背景
    # screen.fill(pygame.image.load('img/start/bk.png').convert())
    screen.blit(get_all_img['st_bk'],(0,0))
    #开始游戏按钮
    if st_bt_is_on[0] == 0:
        screen.blit(start_button_dict['st_game'],game_setting.start_button['st'])
    #设置按钮
    if st_bt_is_on[1] == 0:
        screen.blit(start_button_dict['op_game'],game_setting.start_button['op'])
    #退出按钮
    if st_bt_is_on[2] == 0:
        screen.blit(start_button_dict['ex_game'],game_setting.start_button['ex'])
    pygame.draw.circle(screen, [255, 0, 0], mouse_xy, 5)
    pygame.display.flip()
def start_interface_event(screen,mouse_xy):
    global control_game
    start_button_set = game_setting.start_button
    st_bt_is_on[0] = 0
    st_bt_is_on[1] = 0
    st_bt_is_on[2] = 0
    if mouse_xy[0]> start_button_set['st'][0]+170 and mouse_xy[0]< start_button_set['st'][0] + start_button_set['st_tra'][0]-170:
        if mouse_xy[1] >start_button_set['st'][1]+170 and mouse_xy[1] < start_button_set['st'][1] + start_button_set['st_tra'][1]-170:
            st_bt_is_on[0] = 1
            st_bt_is_on[1] = 0
            st_bt_is_on[2] = 0
    if mouse_xy[0]> start_button_set['op'][0]+140 and mouse_xy[0]< start_button_set['op'][0] + start_button_set['op_tra'][0]-140:
        if mouse_xy[1] >start_button_set['op'][1]+140 and mouse_xy[1] < start_button_set['op'][1] + start_button_set['op_tra'][1]-140:
            st_bt_is_on[0] = 0
            st_bt_is_on[1] = 1
            st_bt_is_on[2] = 0
    if mouse_xy[0]> start_button_set['ex'][0]+110 and mouse_xy[0]< start_button_set['ex'][0] + start_button_set['ex_tra'][0]-110:
        if mouse_xy[1] >start_button_set['ex'][1]+110 and mouse_xy[1] < start_button_set['ex'][1] + start_button_set['ex_tra'][1]-110:
            st_bt_is_on[0] = 0
            st_bt_is_on[1] = 0
            st_bt_is_on[2] = 1





    # start_all_img['start_game']=pygame.transform.rotate(start_all_img['start_game'] , 89)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if st_bt_is_on[0] == 1:
                control_game = 2
                print('----------------')
                    
        if event.type == pygame.QUIT:
            sys.exit(0)

if __name__ == "__main__":
    #pygame初始化
    pygame.init()
    #界面初始化
    screen = pygame.display.set_caption('fuck fruits')
    screen = pygame.display.set_mode((game_setting.screen_width,game_setting.screen_height),pygame.FULLSCREEN|pygame.HWSURFACE)
    clock = pygame.time.Clock()
    #水果精灵组
    all_fruit_group = Group()
    #开始界面使用的图片
    start_button_dict = {
        'st_game':pygame.transform.scale(get_all_img['st_st'],game_setting.start_button['st_tra']),
        'op_game':pygame.transform.scale(get_all_img['st_op'],game_setting.start_button['op_tra']),
        'ex_game':pygame.transform.scale(get_all_img['st_ex'],game_setting.start_button['ex_tra']),
    }
    # screen.blit(pygame.image.load('img/start/bk.png').convert(),(0,0))
    # mouse=pygame.mouse
    mouse_thread = mouse_Thread()
    mouse_thread.start()
    while True:
        clock.tick(30)
        if control_game ==0:
            start_interface_screen(screen,start_button_dict,mouse_thread.mouse_xy)
            start_interface_event(screen,mouse_thread.mouse_xy)
        if control_game == 2:
        # mouse_xy = mouse.get_pos()
            update_event(screen,all_fruit_group,mouse_thread.mouse_xy)
            all_fruit_group.update()
            update_screen(screen,all_fruit_group,mouse_thread.mouse_xy)



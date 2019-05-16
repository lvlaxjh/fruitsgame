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
import img_percess_red
from fruit import Fruits

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
#水果数量
fruit_num = 5
#屏幕分辨率
screen_w = game_setting.screen_width
screen_h = game_setting.screen_height
#
size_f = game_setting.fruit_size
#
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
    return fruit_one
#cv转pygame用
def cvimage_to_pygame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame
def draw_knife(screen,positions):
    pygame.draw.circle(screen, [0, 255, 0], positions, 10)
#主游戏界面更新
def update_game_screen(screen,fruits_group,positions,frame = None):
    screen.fill((0, 0, 0))  # 测试使用,使用调用frame摄像头
    # screen.blit(frame,(0,0))
    
    for i in fruits_group.sprites():
        i.load()
    draw_knife(screen,positions)
    pygame.display.flip()

#主游戏界面事件
def position_determination(fruits_group,positions):
    var = 10
    for fruit_one in all_fruit_group:
        if positions[0]> fruit_one.rect.x+var and positions[0] < fruit_one.rect.x+size_f-var:
            if positions[1]>fruit_one.rect.y+var and positions[1]<fruit_one.rect.y +size_f-var:
                all_fruit_group.remove(fruit_one)
        if fruit_one.rect.y > game_setting.screen_height+250 or fruit_one.rect.x<-250 or fruit_one.rect.x>game_setting.screen_width+250:
                all_fruit_group.remove(fruit_one)

def update_game_event(screen,fruits_group,positions):
    position_determination(fruits_group,positions)
    if len(fruits_group) < fruit_num:
        create_fruit = Fruits(get_fruit(),screen,screen_w,screen_h)
        x_ran = random.randint(size_f,screen_w-size_f)
        create_fruit.set_xy(x_ran, screen_h+size_f)
        fruits_group.add(create_fruit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
def update_start_screen(screen,start_button_dict,positions):
    #背景
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
    draw_knife(screen,positions)
    pygame.display.flip()
def update_start_event(screen,positions):
    global control_game
    start_button_set = game_setting.start_button
    st_bt_is_on[0] = 0
    st_bt_is_on[1] = 0
    st_bt_is_on[2] = 0
    if positions[0]> start_button_set['st'][0]+170 and positions[0]< start_button_set['st'][0] + start_button_set['st_tra'][0]-170:
        if positions[1] >start_button_set['st'][1]+170 and positions[1] < start_button_set['st'][1] + start_button_set['st_tra'][1]-170:
            st_bt_is_on[0] = 1
            st_bt_is_on[1] = 0
            st_bt_is_on[2] = 0
    if positions[0]> start_button_set['op'][0]+140 and positions[0]< start_button_set['op'][0] + start_button_set['op_tra'][0]-140:
        if positions[1] >start_button_set['op'][1]+140 and positions[1] < start_button_set['op'][1] + start_button_set['op_tra'][1]-140:
            st_bt_is_on[0] = 0
            st_bt_is_on[1] = 1
            st_bt_is_on[2] = 0
    if positions[0]> start_button_set['ex'][0]+110 and positions[0]< start_button_set['ex'][0] + start_button_set['ex_tra'][0]-110:
        if positions[1] >start_button_set['ex'][1]+110 and positions[1] < start_button_set['ex'][1] + start_button_set['ex_tra'][1]-110:
            st_bt_is_on[0] = 0
            st_bt_is_on[1] = 0
            st_bt_is_on[2] = 1





    # start_all_img['start_game']=pygame.transform.rotate(start_all_img['start_game'] , 89)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if st_bt_is_on[0] == 1:
                control_game = 2
        if event.type == pygame.QUIT:
            sys.exit(0)

def get_real_positon(position,screen_weidth=game_setting.screen_width):
    return(int((screen_weidth-position[0]*(1920/600))),int(position[1]*(1080/400)))


if __name__ == "__main__":
    #pygame初始化
    pygame.init()
    #界面初始化
    screen = pygame.display.set_caption('fuck fruits')
    screen = pygame.display.set_mode((game_setting.screen_width,game_setting.screen_height),pygame.FULLSCREEN|pygame.HWSURFACE)
    #screen = pygame.display.set_mode((600,400))
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
    mouse=pygame.mouse
    mouse_thread = mouse_Thread()
    mouse_thread.start()

    # cap = cv2.VideoCapture(0)
    while True:
        clock.tick(30)
        get_real_positions = mouse.get_pos()

    # try:
        # ret, frame = cap.read()
        # position = img_percess_red.percess_by_hsv(frame)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = np.rot90(frame)
        # frame = pygame.surfarray.make_surface(frame)
    #     ret, frame = cap.read()


    #     position = img_percess_red.percess_by_hsv(frame)

    #     frame = np.rot90(frame)
    #     frame = pygame.surfarray.make_surface(frame)
        # print(position)
        if control_game ==0:
            update_start_screen(screen,start_button_dict,get_real_positions)
            update_start_event(screen, get_real_positions)
        if control_game == 2:
            # tran_frame = pygame.transform.scale(frame,(game_setting.screen_width,game_setting.screen_height))
            # get_real_positions = get_real_positon(position)
            # update_game_screen(screen,all_fruit_group,get_real_positions,frame=tran_frame)
            update_game_screen(screen,all_fruit_group,get_real_positions)
            all_fruit_group.update()
            update_game_event(screen,all_fruit_group,get_real_positions)
        


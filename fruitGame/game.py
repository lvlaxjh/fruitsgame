import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
import cv2
import numpy as np
import sys
import random
import threading
import time
#
import setting
import img_percess_red
from fruit import Fruits

# 设置
game_setting = setting.Setting()
'''
st_bt_is_on:
    [0]-开始游戏按钮
    [1]-设置按钮
    [2]-退出按钮
        0-显示
        1-强调
'''
st_bt_is_on = [0, 0, 0]  # 开始界面按钮的逻辑
'''
control_game:
    0-初始界面
    1-校准界面(判定红色)
    2-游戏界面
    3-游戏结束界面
    4-设置界面
    5-退出
'''
control_game = 0
# 水果数量
fruit_num = 5
# 屏幕分辨率
screen_w = game_setting.screen_width
screen_h = game_setting.screen_height
#水果尺寸
size_f = game_setting.fruit_size
#时间
game_times = game_setting.game_times
get_times = 0
#分数
score = 0
#判定水果/钟表/青蛙
#全部图片资源
get_all_img = {
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
            'st_bk': pygame.image.load('img/start/bk.jpg'),
            'st_st': pygame.image.load('img/start/st.png'),
            'st_op': pygame.image.load('img/start/op.png'),
            'st_ex': pygame.image.load('img/start/ex.png'),
        }
# 开始界面使用的图片
start_button_dict = {
    'st_game': pygame.transform.scale(get_all_img['st_st'], game_setting.start_button['st_tra']),
    'op_game': pygame.transform.scale(get_all_img['st_op'], game_setting.start_button['op_tra']),
    'ex_game': pygame.transform.scale(get_all_img['st_ex'], game_setting.start_button['ex_tra']),
    'b_st_game': pygame.transform.scale(get_all_img['st_st'], game_setting.start_button['b_st_tra']),
    'b_op_game': pygame.transform.scale(get_all_img['st_op'], game_setting.start_button['b_op_tra']),
    'b_ex_game': pygame.transform.scale(get_all_img['st_ex'], game_setting.start_button['b_ex_tra']),
}
# 鼠标线程
class mouse_Thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mouse_xy = (0, 0)

    def run(self):
        while True:
            self.mouse_xy = pygame.mouse.get_pos()
            # print(self.mouse_xy)

# 随机选取水果
def get_ran_something():
    get_num = random.randint(1, 15)
    num = 'f' +str(get_num)
    fruit_one = get_all_img[num] 
    return fruit_one

#计时
def get_time():
    global get_times,game_times,control_game,score
    time_start = time.time()
    if int(get_times) != int(time_start):
        game_times -= 1
        get_times = time_start
        if game_times == 0:
            game_times = game_setting.game_times
            control_game = 0
            score = 0

def draw_knife(screen, positions):
    pygame.draw.circle(screen, [0, 255, 0], positions, 10)

# 主游戏界面更新
def update_game_screen(screen, fruits_group, positions, time_text,score_text,frame=None):
    screen.fill((0, 0, 0))  # 测试使用,使用调用frame摄像头
    # screen.blit(frame,(0,0))
    get_time()

    time_t_f = time_text.render('time:'+str(game_times),1,(255,0,0))
    score_t_f = score_text.render('score:'+str(score),1,(255,0,0))
    screen.blit(time_t_f,(0,0))
    screen.blit(score_t_f,(500,0))
    for i in fruits_group.sprites():
        i.load()
    draw_knife(screen, positions)



#主游戏界面事件
#切水果判定
def game_position_determination(fruits_group, positions):
    global score
    var = 10
    for fruit_one in all_fruit_group:
        if positions[0] > fruit_one.rect.x+var and positions[0] < fruit_one.rect.x+size_f-var:
            if positions[1] > fruit_one.rect.y+var and positions[1] < fruit_one.rect.y + size_f-var:
                all_fruit_group.remove(fruit_one)
                score+=1
        if fruit_one.rect.y > game_setting.screen_height+500 or fruit_one.rect.x < -500 or fruit_one.rect.x > game_setting.screen_width+500:
            all_fruit_group.remove(fruit_one)

a=0
b=0
def update_game_event(screen, fruits_group, positions):
    global a,b
    game_position_determination(fruits_group, positions)
    # if game_times%5 == 0:
    #     if len(fruits_group) < 2:
    #         create_clock = Fruits(get_all_img['ft'], screen, screen_w, screen_h)
    #         x_ran = random.randint(size_f, screen_w-size_f)
    #         create_clock.set_xy(x_ran, screen_h+size_f)
    #         fruits_group.add(create_clock)
    if len(fruits_group) < fruit_num:
        if game_times%4 == 0 and a ==0:
            create_clock = Fruits(get_all_img['ft'], screen, screen_w, screen_h)
            x_ran = random.randint(size_f, screen_w-size_f)
            create_clock.set_xy(x_ran, screen_h+size_f)
            fruits_group.add(create_clock)
            a+=1
        else:
            a=0
        if game_times%7 == 0 and b ==0:
            create_frog = Fruits(get_all_img['ff'], screen, screen_w, screen_h)
            x_ran = random.randint(size_f, screen_w-size_f)
            create_frog.set_xy(x_ran, screen_h+size_f)
            fruits_group.add(create_frog)
            b+=1
        else:
            b=0
        create_fruit = Fruits(get_ran_something(), screen, screen_w, screen_h)
        x_ran = random.randint(size_f, screen_w-size_f)
        create_fruit.set_xy(x_ran, screen_h+size_f)
        fruits_group.add(create_fruit)
        



#开始游戏界面更新
def update_start_screen(screen, positions):
    # 背景
    screen.blit(get_all_img['st_bk'], (0, 0))
    # 开始游戏按钮
    if st_bt_is_on[0] == 0:
        screen.blit(start_button_dict['st_game'],
                    game_setting.start_button['st'])
    elif st_bt_is_on[0]==1:
        screen.blit(start_button_dict['b_st_game'],
                    game_setting.start_button['b_st'])
    # 设置按钮
    if st_bt_is_on[1] == 0:
        screen.blit(start_button_dict['op_game'],
                    game_setting.start_button['op'])
    elif st_bt_is_on[1]==1:
        screen.blit(start_button_dict['b_op_game'],
                    game_setting.start_button['b_op'])
    # 退出按钮
    if st_bt_is_on[2] == 0:
        screen.blit(start_button_dict['ex_game'],
                    game_setting.start_button['ex'])
    elif st_bt_is_on[2]==1:
        screen.blit(start_button_dict['b_ex_game'],
                    game_setting.start_button['b_ex'])
    draw_knife(screen, positions)

#开始游戏界面事件
def start_position_determination(positions):
    start_button_set = game_setting.start_button
    if positions[0] > start_button_set['st'][0]+170 and positions[0] < start_button_set['st'][0] + start_button_set['st_tra'][0]-170:
        if positions[1] > start_button_set['st'][1]+170 and positions[1] < start_button_set['st'][1] + start_button_set['st_tra'][1]-170:
            st_bt_is_on[0] = 1
            st_bt_is_on[1] = 0
            st_bt_is_on[2] = 0
    if positions[0] > start_button_set['op'][0]+140 and positions[0] < start_button_set['op'][0] + start_button_set['op_tra'][0]-140:
        if positions[1] > start_button_set['op'][1]+140 and positions[1] < start_button_set['op'][1] + start_button_set['op_tra'][1]-140:
            st_bt_is_on[0] = 0
            st_bt_is_on[1] = 1
            st_bt_is_on[2] = 0
    if positions[0] > start_button_set['ex'][0]+110 and positions[0] < start_button_set['ex'][0] + start_button_set['ex_tra'][0]-110:
        if positions[1] > start_button_set['ex'][1]+110 and positions[1] < start_button_set['ex'][1] + start_button_set['ex_tra'][1]-110:
            st_bt_is_on[0] = 0
            st_bt_is_on[1] = 0
            st_bt_is_on[2] = 1
def update_start_event(screen, positions):
    global control_game
    st_bt_is_on[0] = 0
    st_bt_is_on[1] = 0
    st_bt_is_on[2] = 0
    start_position_determination(positions)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if st_bt_is_on[0] == 1:
                control_game = 2
            if st_bt_is_on[1] == 1:
                control_game = 4
            if st_bt_is_on[2] == 1:
                control_game = 5


def get_real_positon(position, screen_weidth=game_setting.screen_width):
    return(int((screen_weidth-position[0]*(1920/600))), int(position[1]*(1080/400)))

if __name__ == "__main__":
    # pygame初始化
    pygame.init()
    # 界面初始化
    screen = pygame.display.set_caption('fuck fruits')
    screen = pygame.display.set_mode(
        (game_setting.screen_width, game_setting.screen_height), pygame.FULLSCREEN | pygame.HWSURFACE)
    clock = pygame.time.Clock()
    # 水果精灵组
    all_fruit_group = Group()
    mouse = pygame.mouse
    mouse_thread = mouse_Thread()
    mouse_thread.start()
    # cap = cv2.VideoCapture(0)
    time_text = pygame.font.SysFont('宋体',100)
    score_text = pygame.font.SysFont('宋体',100)
    while True:
        clock.tick(60)
        # ret, frame = cap.read()
        # position = img_percess_red.percess_by_hsv(frame)
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # frame = np.rot90(frame)
        # frame = pygame.surfarray.make_surface(frame)
        get_real_positions = mouse_thread.mouse_xy

        if control_game == 0:
            update_start_screen(screen, get_real_positions)
            update_start_event(screen, get_real_positions)
        if control_game == 2:
            # tran_frame = pygame.transform.scale(frame,(game_setting.screen_width,game_setting.screen_height))
            # get_real_positions = get_real_positon(position)
            # update_game_screen(screen,all_fruit_group,get_real_positions,frame=tran_frame)
            update_game_screen(screen, all_fruit_group, get_real_positions,time_text,score_text)
            all_fruit_group.update()
            update_game_event(screen, all_fruit_group, get_real_positions)
        if control_game == 5:
            pygame.quit()
            sys.exit(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        pygame.display.flip()

import win32api,win32con
import pygame
#界面设置
class Setting():
    def __init__(self):
        #获取屏幕分辨率
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        #水果尺寸
        self.fruit_size = 300
        #游戏时间
        self.game_times = 30
        #开始界面使用的图片
        self.start_button = {
            'st':(120, 347),
            'op':(673, 433),
            'ex':(1199, 365),
            'b_st':(95, 322),
            'b_op':(648, 408),
            'b_ex':(1174, 340),
            'st_tra': (600,600),
            'op_tra': (500,500),
            'ex_tra': (450,450),
            'b_st_tra': (650,650),
            'b_op_tra': (550,550),
            'b_ex_tra': (500,500),
        }

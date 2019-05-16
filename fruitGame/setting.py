import win32api,win32con
#界面设置
class Setting():
    def __init__(self):
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.fruit_speed = 10

        self.start_button = {
            'st':(120, 347),
            'op':(673, 433),
            'ex':(1199, 365),
            'st_tra': (600,600),
            'op_tra': (500,500),
            'ex_tra': (450,450),
        }

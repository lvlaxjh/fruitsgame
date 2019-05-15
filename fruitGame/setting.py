import win32api,win32con
#界面设置
class Setting():
    def __init__(self):
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.fruit_speed = 10

        self.start_game_img = (350,350)
        self.setting_game_img = (300,300)
        self.esc_game_img = (200,200)

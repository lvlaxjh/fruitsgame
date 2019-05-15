import random
import pygame
import win32api,win32con

class Item():
    def __init__(self, width, height, rate = 1, pos_x = None, pos_y = None, mode = 0):
        self.width = width
        self.height = height
        self.rate = rate
        self.pos_x = random.randint(int(-self.width/5), int(self.width/5) + width) if pos_x == None else pos_x
        self.pos_y = int(self.height * 1.05) if pos_y == None else pos_y
        self.speed_x = self.width/10000 * random.uniform(8, 12) * rate * random.choice([-1, 1])
        self.speed_y = (-1) * self.height/2000 * random.uniform(4, 6) * rate
        self.g = height/50000 * rate
        if mode == 1:
            while self.check() != 1:
                self.refresh()
            self.speed_x *= -1
            self.speed_y *= -1

    def refresh(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.speed_y += self.g
        return (int(self.pos_x), int(self.pos_y))

    def reset(self, rate = 1, pos_x = None, pos_y = None):
        """
        self.pos_x = random.randint(int(-self.width/5), int(self.width/5) + self.width) if pos_x == None else pos_x
        self.pos_y = int(self.height * 0.8) if pos_y == None else pos_y
        self.speed_x = self.width/10000 * random.randint(-8, 8) * rate
        self.speed_y = (-1) * self.height/2000 * random.randint(3, 10) * rate    
        """
        self.__init__(width = self.width, height = self.height, rate = self.rate)

    def check(self):
        """
        返回1说明该item已出界，返回0则说明尚未出界
        """
        if self.pos_x - self.width >= 300 and self.speed_x >= 0:
            return 1
        if self.pos_x <= -300 and self.speed_x <= 0:
            return 1
        if self.pos_y >= self.height+300 and self.speed_y >= 0:
            return 1
        return 0
        

def main():
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    pygame.init()
    clock = pygame.time.Clock()
    area = [800, 600]
    screen = pygame.display.set_mode(area)
    pygame.display.set_caption("PHY")
    time = 10
    items = [Item(800, 600, rate = 2) for i in range(10)]
    while True:
        screen.fill(0)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                pygame.quit()
                exit(0)
        clock.tick(1000)
        for item in items:
            if item.check():
                item.reset()
            (x, y) = item.refresh()
            pygame.draw.circle(screen, [255, 0, 0], [x, y], 10)
            pygame.display.update()
        time += 1

if __name__ == "__main__":
    main()
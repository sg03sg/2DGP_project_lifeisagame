from pico2d import *
import game_world
import game_framework
import background

class Item:
    image = None

    def __init__(self, y):
        if Item.image == None:
            Item.image = load_image('Images/ITEMIMAGE_babymilk.png')
        self.x = 1300
        self.y = y
        self.speed = background.RUN_SPEED_PPS + 500  # 아이템의 속도 (배경보다 빠르게)
        self.xv = -self.speed  # x 축 속도

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def draw(self):
        self.image.draw(self.x, self.y,40,40)
        draw_rectangle(*self.get_bb())

    def handle_collision(self,group, other):
        if group == 'hero:item':
            game_world.remove_object(self)

    def update(self):
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time
        if self.x <= 0:
            game_world.remove_object(self)

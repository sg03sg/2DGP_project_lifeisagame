from pico2d import *
import common
import game_framework
import game_world
import json

with open('Json/button_data.json', 'r', encoding='utf-8') as f:
    h = json.load(f)
hobby_select_data = h['sprites']

SCREEN_HEIGHT = get_canvas_height()
SCREEN_WIDTH = get_canvas_width()
BOTTOM_OFFSET = 100

##동아리 선택 객체를 그리고 충돌 범위를 저장
class Hobby:
    def __init__(self,num = 0):
        self.image = load_image('Images/hobby_select.png')
        self.w = hobby_select_data[num]['width']
        self.h = hobby_select_data[num]['height']
        self.x = 1310
        self.y = SCREEN_HEIGHT // 2 + BOTTOM_OFFSET // 2
        self.num = num

    def update(self):
        self.x -= common.background.display_speed * game_framework.frame_time
        if self.x < - 55:
            game_world.remove_object(self)

    def draw(self):
        i = self.num
        w = self.w
        h = self.h
        self.image.clip_draw(int(hobby_select_data[i]["x"]),
                             int(hobby_select_data[i]['y']),
                             int(hobby_select_data[i]['width']),
                             int(hobby_select_data[i]['height']),
                             self.x + self.w // 2, self.y, w,
                             h)
from pico2d import *
import common
import game_framework
import game_world
import common
import json

with open('Json/hobby_select_data.json', 'r', encoding='utf-8') as f:
    h = json.load(f)
hobby_select_data = h['sprites']

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_OFFSET = 100

select_offset = 20

##선택 시스템 객체 게임월드에 추가를 결정하는 클래스
class Select_System:
    def __init__(self):
        self.hobby = [Hobby(0), Hobby(1), Hobby(2)]

    def select_decision(self,other):
        background = common.background
        pos = other.pos
        if pos <= background.total_run and not other.exist: # <= self.map_total_w[self.stage] + float(gate.gate_size / 2)
            other.exist = True
            game_world.add_object(other, 0)

    def update(self):
        for hobby in self.hobby:
            self.select_decision(hobby)
    def draw(self):
        pass

##동아리 선택 객체를 그리고 충돌 범위를 저장
class Hobby:
    def __init__(self,num = 0):
        self.image = load_image('Images/hobby_select.png')
        self.w = hobby_select_data[num]['width'] * 2
        self.h = hobby_select_data[num]['height'] * 2
        self.x = 1310
        self.y = common.hero.y - 20
        self.num = num
        self.pos = common.background.map_total_w[1] - common.background.frame_w[1] + 80 * (num+1)
        self.exist = False

    def select_collision(self, other):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def get_bb(self):
        half_w = self.w // 2
        half_h = self.h // 2
        return self.x - half_w - select_offset, self.y , self.x + half_w+select_offset, self.y + self.h

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
                             self.x, self.y + self.h //2, w, h)
        draw_rectangle(*self.get_bb())
from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
from state_machine import StateMachine

import game_world
import game_framework

import json

with open('baby_sprite_sheet_data.json', 'r', encoding='utf-8') as f:
    baby_rounding_box_data = json.load(f)

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def jump_end(e):
    return e[0] == 'jump_end'

def No(e):
    return False

def hero_jump(hero, dt):
    hero.jump_vy += hero.gravity * dt
    hero.y += hero.jump_vy * dt
    # 착지 검사
    if hero.y <= 150:
        hero.y = 150
        hero.jump_vy = 0.0
        hero.state_machine.handle_state_event(("jump_end", None))


TIME_PER_ACTION = 0.7 #사람이 뛸때 두걸음 내딛는 평균 시간은 약 0.7초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

class Run:
    def __init__(self,hero):
        self.hero = hero

    def enter(self,e):
        pass

    def exit(self,e):
        pass

    def do(self):
        self.hero.frame = (self.hero.frame+FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)%5
        if self.hero.frame %10 ==0:
            self.hero.y_frame = (self.hero.y_frame +1)%3
    def draw(self):
        i = int(self.hero.frame)
        self.hero.image.clip_draw(int(baby_rounding_box_data['sprites'][i]["x"])+7,int(baby_rounding_box_data['sprites'][i]['y']) ,
                                  int(baby_rounding_box_data['sprites'][i]['width'])-7, int(baby_rounding_box_data['sprites'][i]['height']), self.hero.x, self.hero.y, 100,
                                       100)

class Idle:
    def __init__(self, hero):
        self.hero = hero

    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Jump:
    def __init__(self, hero):
        self.hero = hero

    def enter(self,e):
        # 점프 시작 시 초기 속도 설정
        self.hero.jump_vy = self.hero.jump_initial_v

    def exit(self,e):
        pass

    def do(self):
        dt = game_framework.frame_time
        hero_jump(self.hero, dt)

    def draw(self):
        i = int(self.hero.frame)
        self.hero.image.clip_draw(int(baby_rounding_box_data['sprites'][i]["x"]),
                                  int(baby_rounding_box_data['sprites'][i]['y']),
                                  int(baby_rounding_box_data['sprites'][i]['width']),
                                  int(baby_rounding_box_data['sprites'][i]['height']), self.hero.x, self.hero.y, 100,
                                  100)

class Hero:
    def __init__(self):
        self.x, self.y = 640, 150
        self.frame = -1
        self.y_frame =-1
        self.image = load_image('baby_sprite_sheet.png')

        #ui 관련 값
        self.hp = 100
        self.happy = 50

        # 점프 관련 기본값 : v0^2 / (2 * |g|) <-이거 계산하면 최고 높이
        self.jump_initial_v = 1000.0    # 초기 상승 속도(px/s)
        self.gravity = -2500.0         # 중력(px/s^2)
        self.jump_vy = 0.0

        self.run = Run(self)
        self.idle = Idle(self)
        self.jump = Jump(self)
        self.state_machine = StateMachine(
              self.run,
        {
                self.run: {space_down: self.jump},
                self.jump: {jump_end: self.run},
                self.idle: {No: self.idle},
             }
        )


    def update(self):
        self.state_machine.update()

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        self.state_machine.handle_state_event(("INPUT", event))

    def handle_collision(self,group, other):
        if group == 'hero:item':
            # if self.hp < 100:
            #     self.hp += 5
            if self.happy < 100:
                self.happy += 5
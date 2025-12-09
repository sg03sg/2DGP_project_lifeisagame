from pico2d import load_image, draw_rectangle, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import common
from state_machine import StateMachine

import game_world
import game_framework

import json
hero_rounding_box_data = []
hero_jump_rounding_box_data = []
with open('Json/baby_sprite_sheet_data.json', 'r', encoding='utf-8') as f:
    hero_rounding_box_data.append(json.load(f))

with open('Json/walk_boy1_data.json', 'r', encoding='utf-8') as f:
    hero_rounding_box_data.append(json.load(f))

with open('Json/student_run1_data.json', 'r', encoding='utf-8') as f:
    hero_rounding_box_data.append(json.load(f))

with open('Json/jump_boy_data.json', 'r', encoding='utf-8') as f:
    hero_jump_rounding_box_data.append(json.load(f))

with open('Json/stu_jump_data.json', 'r', encoding='utf-8') as f:
    hero_jump_rounding_box_data.append(json.load(f))

with open('Json/get_hobby_data.json', 'r', encoding='utf-8') as f:
    get_h = json.load(f)
get_hobby_data = get_h['sprites']

scale_hero = []

def scale_hero_def(scale_hero_arr):
    if scale_hero_arr:
        scale_hero_arr.clear()
    for i in range(len(hero_rounding_box_data)):
        age = hero_rounding_box_data[i]['sprites']
        x = max(frame['width'] for frame in age)
        scale_hero_arr.append(x)
scale_hero_def(scale_hero)

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def jump_end(e):
    return e[0] == 'jump_end'

def select(e):
    return e[0] == 'select'
def select_end(e):
    return e[0] == 'select_end'

def hero_jump(hero, dt):
    hero.jump_vy += hero.gravity * dt
    hero.y += hero.jump_vy * dt
    # 착지 검사
    if hero.y <= 150 + int((hero.tall[hero.age]-100)//2):
        hero.y = 150 + int((hero.tall[hero.age]-100)//2)
        hero.jump_vy = 0.0
        hero.state_machine.handle_state_event(("jump_end", None))


TIME_PER_ACTION = [0.6,0.6,0.6,0.6,0.6,0.9] #사람이 뛸때 두걸음 내딛는 평균 시간은 약 0.7초
ACTION_PER_TIME = [1.0 /TPA for TPA in TIME_PER_ACTION]
FRAMES_PER_ACTION = [6,6,6,6,6,4]

class Run:
    def __init__(self,hero):
        self.hero = hero

    def enter(self,e):
        pass

    def exit(self,e):
        pass

    def do(self):
        self.hero.frame = (self.hero.frame+FRAMES_PER_ACTION[self.hero.age] * ACTION_PER_TIME[self.hero.age] * game_framework.frame_time)%self.hero.walk_frame_counts[self.hero.age]
        # if self.hero.frame %10 ==0:
        #     self.hero.y_frame = (self.hero.y_frame +1)%3
    def draw(self):
        i = int(self.hero.frame)
        frame_data = hero_rounding_box_data[self.hero.age]['sprites'][i]
        base_width = scale_hero[self.hero.age]
        scale = self.hero.side_size[self.hero.age] / base_width
        draw_w = int(int(frame_data['width']) * scale)
        self.hero.walk_images[self.hero.age].clip_draw(int(frame_data["x"]),int(frame_data['y']) ,
                                  int(frame_data['width']), int(frame_data['height']), self.hero.x, self.hero.y, draw_w,
                                       self.hero.tall[self.hero.age])

class Earn_hobby:
    def __init__(self, hero):
        self.hero = hero
        self.image = load_image('Images/get_hobby.png')
        self.num = 0

    def enter(self,e):
        self.hero.x = 640
        self.hero.y = 100 + (self.hero.tall[2]+50)//2
        self.time = get_time()
    def exit(self,e):
        common.pause_def.resume_game_switch()
        common.selecting = False

    def do(self):
        pass
    def draw(self):
        if get_time() - self.time > 1.5:
            self.hero.state_machine.handle_state_event(('select_end',None))
            return
        i = self.num
        self.image.clip_draw(int(get_hobby_data[i]["x"]),int(get_hobby_data[i]["y"]),int(get_hobby_data[i]["width"]),int(get_hobby_data[i]["height"]),self.hero.x,100 + (self.hero.tall[2]+50)//2,self.image.h,self.hero.tall[2]+50)

class Jump:
    def __init__(self, hero):
        self.hero = hero

    def enter(self,e):
        # 점프 시작 시 초기 속도 설정
        self.hero.jump_vy = self.hero.jump_initial_v[self.hero.age]
        self.hero.frame = 0

    def exit(self,e):
        pass

    def do(self):
        if  not self.hero.age ==0 and not int(self.hero.frame) == self.hero.jump_frame_counts[self.hero.age-1]-1:
            self.hero.frame = (self.hero.frame + FRAMES_PER_ACTION[self.hero.age] * ACTION_PER_TIME[self.hero.age] * game_framework.frame_time) % self.hero.jump_frame_counts[self.hero.age-1]
        dt = game_framework.frame_time
        hero_jump(self.hero, dt)

    def draw(self):
        i = int(self.hero.frame)
        if self.hero.age ==0:
            frame_data = hero_rounding_box_data[self.hero.age]['sprites'][i]
            base_width = scale_hero[self.hero.age]
            scale = self.hero.side_size[self.hero.age] / base_width
            draw_w = int(int(frame_data['width']) * scale)
            self.hero.walk_images[self.hero.age].clip_draw(int(frame_data["x"]), int(frame_data['y']),
                                                           int(frame_data['width']), int(frame_data['height']),
                                                           self.hero.x, self.hero.y, draw_w,
                                                           self.hero.tall[self.hero.age])
        else:
            age = self.hero.age - 1
            frame_data = hero_jump_rounding_box_data[age]['sprites'][i]
            base_width = scale_hero[self.hero.age]
            scale = 100 / base_width
            draw_w = int(int(frame_data['width']) * scale)
            self.hero.jump_images[age].clip_draw(
                int(frame_data["x"]),int(frame_data['y']), int(frame_data['width']),int(frame_data['height']),
                self.hero.x, self.hero.y, draw_w,
                self.hero.tall[self.hero.age])


class Hero:
    def __init__(self,filename=None):
        if filename is None:
            walk_filename = ['Images/baby_sprite_sheet.png','Images/walk_boy.png','Images/student_run.png']
            jump_filename = ['Images/jump_boy.png','Images/stu_jump.png']

        self.walk_images = [load_image(f) for f in walk_filename]
        self.jump_images = [load_image(f) for f in jump_filename]

        self.tall = [100,140,230,260,260,240]  # 각 나이대별 키
        self.side_size = [100,120,150,160,160,150]  # 각 나이대별 옆 크기
        self.age = 0

        self.walk_frame_counts = [6,6,6,6,6,4]
        self.jump_frame_counts = [3,5,5,5,4]
        self.x,self.y = 640,150
        self.frame = -1
        self.y_frame =-1

        #ui 관련 값
        self.hp = 100
        self.happy = 50
        self.money = 0
        self.smarter = 0
        self.kinder = 0
        self.artistic = 0
        self.smoking = 0

        #직업
        self.job = 0

        # 점프 관련 기본값 : v0^2 / (2 * |g|) <-이거 계산하면 최고 높이
        self.jump_initial_v = [1000.0,1300.0,1300.0,1300.0,1200.0,1200.0]    # 초기 상승 속도(px/s)
        self.gravity = -2500.0         # 중력(px/s^2)
        self.jump_vy = 0.0

        self.run = Run(self)
        self.jump = Jump(self)
        self.earn_hobby = Earn_hobby(self)
        self.state_machine = StateMachine(
              self.run,
        {
                self.run: {space_down: self.jump,select: self.earn_hobby},
                self.jump: {jump_end: self.run,select: self.earn_hobby},
                self.earn_hobby: {select_end: self.run}
             }
        )

        self.stop = False


    def update(self):
        if self.stop:
            return
        self.state_machine.update()

    def get_bb(self):
        box_half_width = int(self.tall[self.age]/2)
        box_half_height = int(self.side_size[self.age]/2)
        return self.x - box_half_height, self.y - box_half_width, self.x + box_half_height, self.y + box_half_width

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

die_data = []
with open("Json/old_die_data.json", 'r', encoding='utf-8') as f:
    die_data.append(json.load(f))
with open("Json/old_die_background_data.json", 'r', encoding='utf-8') as f:
    die_data.append(json.load(f))

class Old_die:
    def __init__(self,filename=None):
        self.die_image = load_image("Images/old_die.png")
        self.die_bg_images = load_image("Images/old_die_background.png")

        # self.die_num = 0
        # self.bg_num = 1

        self.freame_die = 0
        self.frame_bg = 0

        self.w = [180,300]
        self.h = [300,200]

        self.frame_counts = [12,3]
        self.x,self.y = [640,750],[100+self.h[0]//2,150+self.h[1]//2]

        self.TIME_PER_ACTION = 3.0 #엔딩 애니메이션 시간은 3초
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION
        self.FRAMES_PER_ACTION = self.frame_counts

        self.time = get_time()

        self.stop = False

    def update(self):
        if not self.stop:
            self.frame_die = (self.freame_die + self.FRAMES_PER_ACTION[0] * self.ACTION_PER_TIME * game_framework.frame_time) % self.frame_counts[0]
            self.frame_bg = (self.frame_bg + self.FRAMES_PER_ACTION[1] * self.ACTION_PER_TIME * game_framework.frame_time) % self.frame_counts[1]

        if int(self.frame_die) >= self.frame_counts[1]-1:
            self.stop = True

    def draw(self):
        i_0 = int(self.frame_die)
        j_0 = int(self.frame_bg)
        frame_data_0 = die_data[0]['sprites'][i_0]
        frame_data_1 = die_data[1]['sprites'][j_0]
        self.die_image.clip_draw(int(frame_data_0["x"]),
                                 int(frame_data_0['y']),
                                 int(frame_data_0['width']),
                                 int(frame_data_0['height']),
                                 self.x[0], self.y[0], self.w[0], self.h[0])
        self.die_bg_images.clip_draw(int(frame_data_1["x"]),
                                     int(frame_data_1['y']),
                                     int(frame_data_1['width']),
                                     int(frame_data_1['height']),
                                     self.x[1], self.y[1], self.w[1], self.h[1])
from pico2d import *
import game_framework

import play_mode

# 화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
with open('Json/baby_sprite_sheet_data.json', 'r', encoding='utf-8') as f:
    button_rounding_box_data = json.load(f)

class Skillui:
    def __init__(self,name = None):
        if name == 'hobby':
            filename = ["Images/skill_hobby1.png","Images/skill_hobby2.png","Images/skill_hobby3.png",
                        "Images/skill_hobby4.png"]
            self.run = False
            self.images = [load_image(f) for f in filename]
            self. percent = 0
            self.x = 100
            self.kind = 0
            self.json_num = 2
        elif name == 'friend':
            self.image = load_image("Images/skill_friend.png")
            self.run = False
            self.percent = 0
            self.x= 220
            self.json_num = 3
        elif name == 'family':
            self.image = load_image("Images/skill_friend.png")
            self.run = False
            self.percent = 0
            self.x= 340
            self.json_num = 4
        self.name = name
        self.image_H = self.image.h
        self.image_W = self.image.w
        self.y = 60
        self.size = 120

        def update(self):
            # if self.run:
            pass

        def draw(self):
            if self.name == 'hobby':
                self.images[0].clip_draw(button_rounding_box_data['sprites'][self.json_num]["x"],button_rounding_box_data['sprites'][self.json_num]["y"],
                                         button_rounding_box_data['sprites'][self.json_num]["width"],button_rounding_box_data['sprites'][self.json_num]["height"],
                                         self.x,self.y,self.size,self.size)
            else:
                self.image.clip_draw(button_rounding_box_data['sprites'][self.json_num]["x"],button_rounding_box_data['sprites'][self.json_num]["y"],
                                     button_rounding_box_data['sprites'][self.json_num]["width"],button_rounding_box_data['sprites'][self.json_num]["height"],
                                     self.x,self.y,self.size,self.size)

class Itemui:
    def __init__(self,name = None):
        if name == 'baby':
            self.image = load_image("Images/love_baby.png")
            self. percent = play_mode.hero.hp
            self.age = 1
        elif name == 'smart':
            self.image = load_image("Images/ui_smart.png")
            self.percent = play_mode.hero.smart
            self.age = 1
        elif name == 'painting':
            self.image = load_image("Images/ui_painting.png")
            self.percent = play_mode.hero.happy
            self.age = 1
        self.name = name
        self.image_H = self.image.h
        self.image_W = self.image.w

    def update(self):
        pass

    def draw(self):
        pass

class Ui:
    def __init__(self,name,x,age=0):
        if name == 'hp':
            self.image = load_image("Images/hp_bar.png")
            self. percent = play_mode.hero.hp / 100
            self.kind = 0
        elif name == 'happy':
            self.image = load_image("Images/happy_bar.png")
            self.percent = play_mode.hero.happy / 100
            self.kind =1
        self.image_H = self.image.h
        self.image_W = self.image.w
        self.x = x
        self.y = SCREEN_HEIGHT -50

    def update(self):
        if self.kind == 0:
            self.percent = play_mode.hero.hp / 100
        elif self.kind ==1:
            self.percent = play_mode.hero.happy / 100

    def draw(self):
        head_img_w = 12
        head_scr_w = 30
        blank = 5
        bar_dst_w = 80

        # 이미지 모양 그리기: self.x는 모양의 중심 좌표
        self.image.clip_draw(0, 0, head_img_w, self.image_H, self.x, self.y, head_scr_w, 40)

        # 게이지 그리기 왼쪽 고정 => 오른쪽으로만 확장
        p = self.percent
        src_w = int((self.image_W - head_img_w) * p)
        dst_w = int(bar_dst_w * p)

        left_edge = self.x + (head_scr_w / 2) + blank
        center_x = left_edge + (dst_w / 2)

        self.image.clip_draw(head_img_w, 0, src_w, self.image_H, center_x, self.y, dst_w, 40)

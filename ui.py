from pico2d import *
import game_framework

import play_mode

# 화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

with open('Json/button_data.json', 'r', encoding='utf-8') as f:
    button_data = json.load(f)
with open('Json/ui_data.json', 'r', encoding='utf-8') as f:
    ui_data = json.load(f)
with open('Json/number_data.json', 'r', encoding='utf-8') as f:
    number_data = json.load(f)

slash = number_data['sprites'][10]

class Skillui:
    def __init__(self,name = None):
        if name == 'hobby':
            self.run = False
            self. percent = 0
            self.x = 100
            self.kind = 0
            self.json_num = 2
        elif name == 'friend':
            self.run = False
            self.percent = 0
            self.x= 220
            self.json_num = 3
        elif name == 'family':
            self.run = False
            self.percent = 0
            self.x= 340
            self.json_num = 4
        self.image = load_image("Images/button.png")
        self.name = name
        self.y = 60
        self.size = 100

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(int(button_data['sprites'][self.json_num]["x"]),int(button_data['sprites'][self.json_num]["y"]),
                                 int(button_data['sprites'][self.json_num]["width"]),int(button_data['sprites'][self.json_num]["height"]),
                                 self.x,self.y,self.size,self.size)

class Age1ui:
    def __init__(self,name = None):
        self.image = load_image("Images/ui.png")
        self.number_img = load_image("Images/number.png")
        self.name = name
        self.size = 10
        if name == 'smart':
            self.count = play_mode.hero.smarter
            self.json_num = 2
            self.x,self.y = 410,70
            self.num = 0
        elif name == 'baby':
            self.count = play_mode.hero.kinder
            self.json_num = 3
            self.x,self.y = 510,70
            self.num = 1
        elif name == 'painting':
            self.count = play_mode.hero.artistic
            self.json_num = 4
            self.x,self.y = 410,73 + self.size
            self.num = 2
        self.space_num = 5
        self.spacing =2
        self.num_size = self.size - self.spacing

    def update(self):
        pass

    def draw(self):
        #아이콘
        self.image.clip_draw(int(ui_data['sprites'][self.json_num]["x"]),
                             int(ui_data['sprites'][self.json_num]["y"]),
                             int(ui_data['sprites'][self.json_num]["width"]),
                             int(ui_data['sprites'][self.json_num]["height"]),
                             self.x, self.y, self.size, self.size)
        #숫자
        x = self.x + self.space_num
        y = self.y - self.spacing
        #2자리 수일때
        if self.count >=10:
            tens = self.count //10
            units = self.count %10
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                 int(number_data['sprites'][tens]["y"]),
                                 int(number_data['sprites'][tens]["width"]),
                                 int(number_data['sprites'][tens]["height"]),
                                 x, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                 int(number_data['sprites'][units]["y"]),
                                 int(number_data['sprites'][units]["width"]),
                                 int(number_data['sprites'][units]["height"]),
                                 x+int(self.spacing//2), y, self.num_size, self.num_size)
        #1자리 수일때
        else:
            i= self.count
            self.image.clip_draw(int(number_data['sprites'][i]["x"]),
                                 int(number_data['sprites'][i]["y"]),
                                 int(number_data['sprites'][i]["width"]),
                                 int(number_data['sprites'][i]["height"]),
                                 x, y, self.num_size, self.num_size)
        x += self.spacing
        #슬래시
        self.image.clip_draw(int(slash["x"]),int(slash["y"]),int(slash["width"]),int(slash["height"]),x, y, self.num_size,self.num_size)
        x += self.spacing
        #최대 숫자
        i = play_mode.uilist.age1ui_max_count[self.num]
        self.image.clip_draw(int(number_data['sprites'][i]["x"]),
                             int(number_data['sprites'][i]["y"]),
                             int(number_data['sprites'][i]["width"]),
                             int(number_data['sprites'][i]["height"]),
                             x, y, self.num_size, self.num_size)







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

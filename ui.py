from pico2d import *
import game_framework

import play_mode
import common
import savelist

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

class Ageui:
    def __init__(self,age=0):
        if age ==1:
            self.uis = [Age1ui(i) for i in savelist.age1uiname]
        elif age ==2:
            self.uis = [Age2ui(i) for i in savelist.age2uiname]
        else:
            self.uis = []
        self.i = len(self.uis)
        self.age = age

    def update(self,age=0):
        if self.age == age:
            if not self.uis:
                return
            for ui in self.uis:
                ui.update()
        else:
            self.uis.clear()
            self.i = 0
            self.age = age

            if age == 1:
                self.uis = [Age1ui(i) for i in savelist.age1uiname]
            elif age == 2:
                self.uis = [Age2ui(i) for i in savelist.age2uiname]
            else:
                self.uis = []
            self.i = len(self.uis)


    def draw(self):
        if not self.uis:
            return
        for ui in self.uis:
            ui.draw()

class Age1ui:
    def __init__(self,name = None):
        self.image = load_image("Images/ui.png")
        self.number_img = load_image("Images/number.png")
        self.name = name
        self.size = 20
        if name == 'smart':
            self.count = common.hero.smarter
            self.json_num = 2
            self.x,self.y = 510,55
            self.num = 0
        elif name == 'baby':
            self.count = common.hero.kinder
            self.json_num = 3
            self.x,self.y = 610,55
            self.num = 1
        elif name == 'painting':
            self.count = common.hero.artistic
            self.json_num = 4
            self.x,self.y = 510,52 - self.size
            self.num = 2
        self.num_size = self.size * 0.8
        self.spacing = self.num_size //2 + 5

    def update(self):
        if self.num == 0:
            self.count = common.hero.smarter
        elif self.num ==1:
            self.count = common.hero.kinder
        elif self.num ==2:
            self.count = common.hero.artistic

    def draw(self):
        #아이콘
        self.image.clip_draw(int(ui_data['sprites'][self.json_num]["x"]),
                             int(ui_data['sprites'][self.json_num]["y"]),
                             int(ui_data['sprites'][self.json_num]["width"]),
                             int(ui_data['sprites'][self.json_num]["height"]),
                             self.x, self.y, self.size, self.size)
        #숫자
        x = self.x + self.size//2 + self.spacing+ 10
        y = self.y
        #2자리 수일때
        if self.count >=10:
            tens = self.count //10
            units = self.count %10
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                 int(number_data['sprites'][tens]["y"]),
                                 int(number_data['sprites'][tens]["width"]),
                                 int(number_data['sprites'][tens]["height"]),
                                 x-self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                 int(number_data['sprites'][units]["y"]),
                                 int(number_data['sprites'][units]["width"]),
                                 int(number_data['sprites'][units]["height"]),
                                 x, y, self.num_size, self.num_size)
        #1자리 수일때
        else:
            i= self.count
            self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                                 int(number_data['sprites'][i]["y"]),
                                 int(number_data['sprites'][i]["width"]),
                                 int(number_data['sprites'][i]["height"]),
                                 x, y, self.num_size, self.num_size)
        x += self.spacing
        #슬래시
        self.number_img.clip_draw(int(slash["x"]),int(slash["y"]),int(slash["width"]),int(slash["height"]),x, y, self.num_size,self.num_size)
        x += self.spacing
        #최대 숫자
        i = savelist.age1ui_max_count[self.num]
        self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                             int(number_data['sprites'][i]["y"]),
                             int(number_data['sprites'][i]["width"]),
                             int(number_data['sprites'][i]["height"]),
                             x, y, self.num_size, self.num_size)

class Age2ui:
    def __init__(self, name=None):
        self.image = load_image("Images/ui.png")
        self.number_img = load_image("Images/number.png")
        self.name = name
        self.size = 20
        if name == 'study':
            self.count = common.hero.smarter
            self.json_num = 5
            self.x, self.y = 510, 55
            self.num = 0
        elif name == 'paint':
            self.count = common.hero.kinder
            self.json_num = 6
            self.x, self.y = 610, 55
            self.num = 1
        elif name == 'music':
            self.count = common.hero.artistic
            self.json_num = 7
            self.x, self.y = 510, 52 - self.size
            self.num = 2
        elif name == 'soccer':
            self.count = common.hero.artistic
            self.json_num = 8
            self.x, self.y = 610, 52 - self.size
            self.num = 3

        self.num_size = self.size * 0.8
        self.spacing = self.num_size // 2 + 5

    def update(self):
        if self.num == 0:
            self.count = common.job_stat.stats[self.num]
        elif self.num == 1:
            self.count = common.job_stat.stats[self.num]
        elif self.num == 2:
            self.count = common.job_stat.stats[self.num]
        elif self.num == 3:
            self.count = common.job_stat.stats[self.num]

    def draw(self):
        # 아이콘
        self.image.clip_draw(int(ui_data['sprites'][self.json_num]["x"]),
                             int(ui_data['sprites'][self.json_num]["y"]),
                             int(ui_data['sprites'][self.json_num]["width"]),
                             int(ui_data['sprites'][self.json_num]["height"]),
                             self.x, self.y, self.size, self.size)
        # 숫자
        x = self.x + self.size // 2 + self.spacing + 10
        y = self.y
        # 2자리 수일때
        if self.count >= 10:
            tens = self.count // 10
            units = self.count % 10
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                      int(number_data['sprites'][tens]["y"]),
                                      int(number_data['sprites'][tens]["width"]),
                                      int(number_data['sprites'][tens]["height"]),
                                      x - self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                      int(number_data['sprites'][units]["y"]),
                                      int(number_data['sprites'][units]["width"]),
                                      int(number_data['sprites'][units]["height"]),
                                      x, y, self.num_size, self.num_size)
        # 1자리 수일때
        else:
            i = self.count
            self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                                      int(number_data['sprites'][i]["y"]),
                                      int(number_data['sprites'][i]["width"]),
                                      int(number_data['sprites'][i]["height"]),
                                      x, y, self.num_size, self.num_size)
        x += self.spacing
        # 슬래시
        self.number_img.clip_draw(int(slash["x"]), int(slash["y"]), int(slash["width"]), int(slash["height"]), x, y,
                                  self.num_size, self.num_size)
        x += self.spacing
        # 최대 숫자
        i = savelist.age2ui_max_count[self.num]
        self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                                  int(number_data['sprites'][i]["y"]),
                                  int(number_data['sprites'][i]["width"]),
                                  int(number_data['sprites'][i]["height"]),
                                  x, y, self.num_size, self.num_size)

class Age3ui:
    def __init__(self, name=None):
        self.image = load_image("Images/ui.png")
        self.number_img = load_image("Images/number.png")
        self.name = name
        self.size = 20
        if name == 'study':
            self.count = common.hero.smarter
            self.json_num = 5
            self.x, self.y = 510, 55
            self.num = 0

        self.num_size = self.size * 0.8
        self.spacing = self.num_size // 2 + 5

    def update(self):
        if self.num == 0:
            self.count = common.job_stat.stats[self.num]
        elif self.num == 1:
            self.count = common.job_stat.stats[self.num]
        elif self.num == 2:
            self.count = common.job_stat.stats[self.num]
        elif self.num == 3:
            self.count = common.job_stat.stats[self.num]

    def draw(self):
        # 아이콘
        self.image.clip_draw(int(ui_data['sprites'][self.json_num]["x"]),
                             int(ui_data['sprites'][self.json_num]["y"]),
                             int(ui_data['sprites'][self.json_num]["width"]),
                             int(ui_data['sprites'][self.json_num]["height"]),
                             self.x, self.y, self.size, self.size)
        # 숫자
        x = self.x + self.size // 2 + self.spacing + 10
        y = self.y
        # 2자리 수일때
        if self.count >= 10:
            tens = self.count // 10
            units = self.count % 10
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                      int(number_data['sprites'][tens]["y"]),
                                      int(number_data['sprites'][tens]["width"]),
                                      int(number_data['sprites'][tens]["height"]),
                                      x - self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                      int(number_data['sprites'][units]["y"]),
                                      int(number_data['sprites'][units]["width"]),
                                      int(number_data['sprites'][units]["height"]),
                                      x, y, self.num_size, self.num_size)
        # 1자리 수일때
        else:
            i = self.count
            self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                                      int(number_data['sprites'][i]["y"]),
                                      int(number_data['sprites'][i]["width"]),
                                      int(number_data['sprites'][i]["height"]),
                                      x, y, self.num_size, self.num_size)
        x += self.spacing
        # 슬래시
        self.number_img.clip_draw(int(slash["x"]), int(slash["y"]), int(slash["width"]), int(slash["height"]), x, y,
                                  self.num_size, self.num_size)
        x += self.spacing
        # 최대 숫자
        i = savelist.age2ui_max_count[self.num]
        self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                                  int(number_data['sprites'][i]["y"]),
                                  int(number_data['sprites'][i]["width"]),
                                  int(number_data['sprites'][i]["height"]),
                                  x, y, self.num_size, self.num_size)







class Ui:
    def __init__(self,name,x,age=0):
        if name == 'hp':
            self.image = load_image("Images/hp_bar.png")
            self. percent = common.hero.hp / 100
            self.kind = 0
        elif name == 'happy':
            self.image = load_image("Images/happy_bar.png")
            self.percent = common.hero.happy / 100
            self.kind =1
        self.image_H = self.image.h
        self.image_W = self.image.w
        self.x = x
        self.y = SCREEN_HEIGHT -50

    def update(self):
        if self.kind == 0:
            self.percent = common.hero.hp / 100
        elif self.kind ==1:
            self.percent = common.hero.happy / 100

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


class Money_ui:
    def __init__(self, name=None):
        self.image = load_image("Images/ui.png")
        self.number_img = load_image("Images/number.png")
        self.name = name
        self.size = 30
        if name == 'coin':
            self.count = common.hero.money
            self.json_num = 0
            self.x, self.y = SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT -50
            self.num = 0

        self.num_size = self.size * 0.7
        self.spacing = self.num_size // 2 + 5

    def update(self):
        self.count = common.hero.money

    def draw(self):
        # 아이콘
        self.image.clip_draw(int(ui_data['sprites'][self.json_num]["x"]),
                             int(ui_data['sprites'][self.json_num]["y"]),
                             int(ui_data['sprites'][self.json_num]["width"]),
                             int(ui_data['sprites'][self.json_num]["height"]),
                             self.x, self.y, self.size, self.size)
        # 숫자
        x = self.x + self.size // 2 + self.spacing + 10
        y = self.y

        ##4자리 수일때
        if self.count >= 1000:
            thousands = self.count // 1000
            hundreds = (self.count // 100) % 10
            tens = ((self.count // 10) % 100) % 10
            units = self.count % 10
            self.number_img.clip_draw(int(number_data['sprites'][thousands]["x"]),
                                      int(number_data['sprites'][thousands]["y"]),
                                      int(number_data['sprites'][thousands]["width"]),
                                      int(number_data['sprites'][thousands]["height"]),
                                      x - self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][hundreds]["x"]),
                                      int(number_data['sprites'][hundreds]["y"]),
                                      int(number_data['sprites'][hundreds]["width"]),
                                      int(number_data['sprites'][hundreds]["height"]),
                                      x, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                      int(number_data['sprites'][tens]["y"]),
                                      int(number_data['sprites'][tens]["width"]),
                                      int(number_data['sprites'][tens]["height"]),
                                      x + self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                      int(number_data['sprites'][units]["y"]),
                                      int(number_data['sprites'][units]["width"]),
                                      int(number_data['sprites'][units]["height"]),
                                      x + (2*self.spacing), y, self.num_size, self.num_size)

        # 3자리 수일때
        elif self.count >= 100:
            hundreds = self.count // 100
            tens = (self.count // 10) % 10
            units = self.count % 10
            self.number_img.clip_draw(int(number_data['sprites'][hundreds]["x"]),
                                      int(number_data['sprites'][hundreds]["y"]),
                                      int(number_data['sprites'][hundreds]["width"]),
                                      int(number_data['sprites'][hundreds]["height"]),
                                      x - self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                      int(number_data['sprites'][tens]["y"]),
                                      int(number_data['sprites'][tens]["width"]),
                                      int(number_data['sprites'][tens]["height"]),
                                      x , y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                      int(number_data['sprites'][units]["y"]),
                                      int(number_data['sprites'][units]["width"]),
                                      int(number_data['sprites'][units]["height"]),
                                      x + self.spacing, y, self.num_size, self.num_size)
        # 2자리 수일때
        elif self.count >= 10:
            tens = self.count // 10
            units = self.count % 10
            self.number_img.clip_draw(int(number_data['sprites'][tens]["x"]),
                                      int(number_data['sprites'][tens]["y"]),
                                      int(number_data['sprites'][tens]["width"]),
                                      int(number_data['sprites'][tens]["height"]),
                                      x - self.spacing, y, self.num_size, self.num_size)
            self.number_img.clip_draw(int(number_data['sprites'][units]["x"]),
                                      int(number_data['sprites'][units]["y"]),
                                      int(number_data['sprites'][units]["width"]),
                                      int(number_data['sprites'][units]["height"]),
                                      x, y, self.num_size, self.num_size)
        # 1자리 수일때
        else:
            i = self.count
            self.number_img.clip_draw(int(number_data['sprites'][i]["x"]),
                                      int(number_data['sprites'][i]["y"]),
                                      int(number_data['sprites'][i]["width"]),
                                      int(number_data['sprites'][i]["height"]),
                                      x, y, self.num_size, self.num_size)
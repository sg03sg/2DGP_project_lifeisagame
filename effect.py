import common
from pico2d import *
import time
import game_framework
import game_world

##이펙트 시간
TIME_PER_ACTION = 2.0
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION

skill_hobby_data = []
with open('Json/skill_hobby1_data.json', 'r', encoding='utf-8') as f:
    skill_hobby_data.append(json.load(f))
with open('Json/skill_hobby2_data.json', 'r', encoding='utf-8') as f:
    skill_hobby_data.append(json.load(f))

class Effect:
    def skill_effect_play(self,skillnum):
        if skillnum == 0:
            effect = Hobby_effect(common.hobby_num)
            game_world.add_object(effect,1)
        else:
            pass

class Hobby_effect:
    def __init__(self,num):
        images = ["Images/skill_hobby1.png", "Images/skill_hobby2.png", "Images/skill_hobby3.png"]
        self.hobby_num = common.hobby_num
        self.duration = 2.0
        self.start_time = time.time()
        self.active = True
        self.images = [load_image(f) for f in images]
        self.frame_count = [6, 6, 1]
        self.frame = 0

        if num ==0:
            self.x,self.y = common.hero.x + common.hero.side_size[common.hero.age], common.hero.y + common.hero.tall[common.hero.age] //2 - 20
        elif num ==1:
            self.x,self.y = common.hero.x+ 10, common.hero.y
        else:
            self.x,self.y = common.hero.x + common.hero.side_size[common.hero.age], 110
        self.num = num
        self.size_w = [80,120,50]
        self.size_h = [70,50,50]

    def update(self):
        if self.num in (0,1):
            if int(self.frame) >= self.frame_count[self.num] - 1:
                game_world.remove_object(self)
                del self
                return
            self.frame = (self.frame + self.frame_count[self.num] * ACTION_PER_TIME * game_framework.frame_time) % self.frame_count[self.num]
            if self.num == 0:
                self.y = common.hero.y + common.hero.tall[common.hero.age] // 2 - 20
            elif self.num == 1:
                self.y = common.hero.y

    def draw(self):
        if self.num in (0,1):
            i = int(self.frame)
            frame_data = skill_hobby_data[self.num]['sprites'][i]
            self.images[self.num].clip_draw(int(frame_data["x"]), int(frame_data['y']),
                                            int(frame_data['width']), int(frame_data['height']),
                                            self.x, self.y, self.size_w[self.num], self.size_h[self.num])
        elif self.num == 2:
            self.images[self.num].draw(self.x, self.y, self.size_w, self.size_h)
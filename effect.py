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
    skill_hobby_data.append(f)
with open('Json/skill_hobby2_data.json', 'r', encoding='utf-8') as f:
    skill_hobby_data.append(f)

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
        self.image = load_image(f'Images/hobby_effect_{self.hobby_num}.png')
        self.duration = 2.0
        self.start_time = time.time()
        self.active = True
        self.images = [load_image(f) for f in images]
        self.frame_count = [6, 6, 1]
        self.frame = 0

        self.x,self.y = common.hero.x + common.hero.side_size[common.hero.age], common.hero.y + common.hero.tall[common.hero.age]
        self.num = num
        self.size_w = images[self.num].w *1.5
        self.size_h = images[self.num].h *1.5

    def update(self):
        if self.num in (0,1):
            if int(self.frame) >= self.frame_count[self.num]:
                game_world.remove_object(self)
                del self
            self.frame = (self.frame + self.frame_count[self.num] * ACTION_PER_TIME * game_framework.frame_time) % self.frame_count[self.num]

    def draw(self):
        if self.num in (0,1):
            i = int(self.frame)
            frame_data = skill_hobby_data[self.num]['sprites'][i]
            self.images[self.num].clip_draw(int(frame_data["x"]), int(frame_data['y']),
                                            int(frame_data['width']), int(frame_data['height']),
                                            self.x, self.y, self.size_w, self.size_h)
        elif self.num == 2:
            self.images[self.num].draw(self.x, self.y, self.size_w, self.size_h)
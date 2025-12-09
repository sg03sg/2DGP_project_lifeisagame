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

with open('Json/f_call_data.json', 'r', encoding='utf-8') as f:
    f_call = json.load(f)

f_call_data = f_call['sprites']

class Effect:
    def skill_effect_play(self,skillnum):
        if skillnum == 0:
            effect = Hobby_effect(common.hobby_num)
            game_world.add_object(effect,1)
        if skillnum == 1:
            effect = Call_effect()
            game_world.add_object(effect,1)
        else:
            pass


PIXEL_PER_METER = (10.0 / 0.9)  # 10 pixel 10 cm
GRAVITY = 120  # m/s^2

class Call_effect:
    def __init__(self):
        self.image = load_image("Images/f_call.png")
        self.duration = 4.0
        self.start_time = get_time()
        self.num = max(0,common.hero.age - 2)
        self.x,self.y = common.hero.x + common.hero.side_size[common.hero.age] - 5, common.hero.y + common.hero.tall[common.hero.age] //2 - 10
        self.size_w = 120
        self.size_h = 100

    def update(self):
        if get_time() - self.start_time >= self.duration:
            game_world.remove_object(self)
            del self
            return
        self.y = common.hero.y + common.hero.tall[common.hero.age] // 2 - 20

    def draw(self):
        i = f_call_data[self.num]
        self.image.clip_draw(int(i["x"]), int(i['y']),
                                        int(i['width']), int(i['height']),
                                        self.x, self.y, self.size_w, self.size_h)

class Hobby_effect:
    def __init__(self,num):
        images = ["Images/skill_hobby1.png", "Images/skill_hobby2.png", "Images/skill_hobby3.png"]
        self.hobby_num = common.hobby_num
        self.duration = 8.0
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
            self.x,self.y = common.hero.x + common.hero.side_size[common.hero.age] - 15, common.hero.y
        self.num = num
        self.size_w = [80,120,50]
        self.size_h = [70,50,50]

        self.yv = 60
        self.ball_count = 0

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
        elif self.num == 2:
            if self.ball_count >= 2:
                game_world.remove_object(self)
                del self
                return

            if self.y < 110:
                self.y = 110
                self.ball_count += 1
                self.yv = 55

            self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
            self.yv -= GRAVITY * game_framework.frame_time

    def draw(self):
        if self.num in (0,1):
            i = int(self.frame)
            frame_data = skill_hobby_data[self.num]['sprites'][i]
            self.images[self.num].clip_draw(int(frame_data["x"]), int(frame_data['y']),
                                            int(frame_data['width']), int(frame_data['height']),
                                            self.x, self.y, self.size_w[self.num], self.size_h[self.num])
        elif self.num == 2:
            self.images[self.num].draw(self.x, self.y, self.size_w[self.num], self.size_h[self.num])



class Item_effect():
    def __init__(self, num):
        images = ["Images/skill_hobby1.png", "Images/skill_hobby2.png", "Images/skill_hobby3.png"]
        if num >= 0:
            self.image = load_image('Images/happy_effect.png')
        if num < 0:
            self.image = load_image('Images/not_happy_effect.png')
        self.start_time = get_time()
        self.x, self.y = common.hero.x + common.hero.side_size[common.hero.age] - 20 , common.hero.y + \
                             common.hero.tall[common.hero.age] // 2 - 30
        self.size_w = 40
        self.size_h = 40

        self.yv = 15

    def update(self):
        if get_time() - self.start_time >= 0.5:
            game_world.remove_object(self)
            del self
            return

        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

    def draw(self):
        self.image.draw(self.x, self.y, self.size_w, self.size_h)
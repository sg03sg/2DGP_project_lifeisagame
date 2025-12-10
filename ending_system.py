from pico2d import *
import common
import game_framework
import game_world
import savelist
from hero import Old_die
import title_mode

with open('Json/curtain_data.json', 'r', encoding='utf-8') as f:
    cutain = json.load(f)
curtain_data = cutain['sprites']

class Ending_system:
    def __init__(self):
        self.ending_image = None
        self.perfect = False
        self.smokken = False
        self.sucide = False

        self.ending = False
        self.time = float('inf')

    def ending_judge(self):
        if self.ending:
            if get_time() - self.time >= 3.0:
                curtain = Curtain()
                game_world.add_object(curtain,3)

        else:
            if self.perfect:
                self.ending_start()
                animation = Old_die()
                game_world.remove_object(common.hero)
                game_world.add_object(animation, 1)

            elif self.smokken:
                game_over = Game_over(1)
                self.ending_start()
                game_world.add_object(game_over, 2)

            elif self.sucide:
                game_over = Game_over(0)
                self.ending_start()
                game_world.add_object(game_over, 2)

    def ending_start(self):
        common.pause_def.pause_game_switch()
        self.time = get_time()
        self.ending = True

    def update(self):
        bg = common.background
        hero = common.hero
        if hero.smoking >= savelist.age3and4ui_max_count[0]:
            self.smokken = True
        elif hero.happy <= 0:
            self.sucide = True
        elif bg.map_idx == 15 and bg.hero_pos >= bg.total_w[19]//2:
            self.perfect = True

        self.ending_judge()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_OFFSET = 100


class Game_over():
    def __init__(self,num):
        filename = ["Images/suicide.png","Images/smokeen_ending.png"]
        self.images = [load_image(f) for f in filename]
        self.scale_x, self.scale_y = SCREEN_WIDTH / self.images[num].w, SCREEN_HEIGHT/ self.images[num].h
        self.x, self.y = self.images[num].w * self.scale_x //2 , self.images[num].h * self.scale_y //2
        self.w, self.h = self.images[num].w * self.scale_x, self.images[num].h * self.scale_y
        self.num = num

    def update(self):
        pass

    def draw(self):
        self.images[self.num].draw(self.x,self.y,self.w,self.h)

TIME_PER_ACTION = 2.0 #커튼 닫힐때 2초
ACTION_PER_TIME = 1.0 /TIME_PER_ACTION
FRAMES_PER_ACTION = 11

class Curtain():
    def __init__(self):
        filename = ["Images/curtain1.png","Images/curtain2.png","Images/curtain3.png"]
        self.images = [load_image(f) for f in filename]
        self.time = get_time()
        self.frame_move = True
        self.frame = 0

    def update(self):
        if get_time() - self.time >= 3.0:
            print('end')
            del common.hero
            game_framework.change_mode(title_mode)
        if not self.frame_move:
            return
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 11
        if int(self.frame) >= 9:
            frame_move = False

    def draw(self):
        start_index = [4,7,11]
        i = int(self.frame)
        img_i = 0
        for idx,val in enumerate(start_index):
            if i < val:
                img_i = idx
                break
        frame_data = curtain_data[i]
        self.images[img_i].clip_draw(int(frame_data["x"]),int(frame_data["y"]),int(frame_data["width"]),int(frame_data["height"]),SCREEN_WIDTH//2,SCREEN_HEIGHT//2,1280,720)
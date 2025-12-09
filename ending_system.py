from pico2d import *
import common
import game_framework
import game_world
import savelist
from background import BOTTOM_OFFSET
from hero import Old_die

class Ending_system:
    def __init__(self):
        self.ending_image = None
        self.perfect = False
        self.smokeen = False
        self.sucide = False

        self.ending = False
        self.time = float('inf')

    def ending_judge(self):
        if self.ending:
            if get_time() - self.time >= 4.0:
                game_framework.change_mode(ending_mode)

        else:
            if self.perfect:
                self.ending_start()
                animation = Old_die()
                game_world.remove_object(common.hero)
                game_world.add_object(animation, 1)

            elif self.smokken:
                game_over = Game_over(1)
                self.ending_start()

            elif self.sucide:
                game_over = Game_over(0)
                self.ending_start()

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
        elif bg.map_idx == 15 and bg.hero_pos == bg.total_w[19]:
            self.perfect = True

    def draw(self):
        pass

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Game_over():
    def __init__(self,num):
        filename = ["Images/game_over.png","Images/smokeen_ending.png"]
        self.images = [load_image(f) for f in filename]
        self.scale_x, self.scale_y = SCREEN_WIDTH / self.images[num].w, (SCREEN_HEIGHT -BOTTOM_OFFSET) / self.images[num].h
        self.x, self.y = self.images[num] * self.scale_x //2 , self.images[num].h * self.scale_y //2
        self.w, self.h = self.images[num].w * self.scale_x, self.images[num].h * self.scale_y
        self.num = num

    def update(self):
        pass

    def draw(self):
        self.images[self.num].draw(self.x,self.y,self.w,self.h)
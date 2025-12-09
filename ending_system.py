from pico2d import *
import common
import game_framework
import game_world
import savelist
from hero import Old_die

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
            if get_time() - self.time >= 4.0:
                game_framework.change_mode(endind_mode)

        else:
            if self.perfect:
                self.ending_start()
                animation = Old_die()
                game_world.remove_object(common.hero)
                game_world.add_object(animation, 1)

            elif self.smokken:
                self.ending_start()

            elif self.sucide:
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

class game_over
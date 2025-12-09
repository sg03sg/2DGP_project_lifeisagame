import time
import common
from pico2d import *

class Skill_system():
    def __init__(self):
        self.skills = common.skills
        self.cooltime = 6.0
        self.last_use_time = [0 for _ in range(len(self.skills))]
        self.can_skill_use = [True for _ in range(len(self.skills))]

    ##스킬 쿨타임 계산 쿨타임 일때는 스킬 쿨타임 상태 ui로 바꾸고 아닐때는 스킬 ui 활성화 상태
    def skill_on_off_switch(self, skill_num):
        if self.skills[skill_num].skill_earn == False:
            return
        current_time = time.time()
        if current_time - self.last_use_time[skill_num] >= self.cooltime:
           self.skills[skill_num].skill_on = True

        else:
            self.skills[skill_num].skill_on = False

    def skill_use(self,skill_num):
        if self.skills[skill_num].skill_earn == False:
            return
        if self.skills[skill_num].skill_on:
            common.effect.skill_effect_play(skill_num)
            self.last_use_time[skill_num] = time.time()
            self.skills[skill_num].on = False
            common.hero.happy = min(100, common.hero.happy + 10)
    def update(self):
        for i in range(len(self.skills)):
            self.skill_on_off_switch(i)

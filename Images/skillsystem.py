import time
import common
from pico2d import *

class SkillSystem():
    def __init__(self):
        self.skills = common.skills
        self.cooltime = 3.0
        self.last_use_time = time.time()
        self.can_skill_use = [True for _ in range(len(self.skills))]

    ##스킬 쿨타임 계산 쿨타임 일때는 스킬 쿨타임 상태 ui로 바꾸고 아닐때는 스킬 ui 활성화 상태
    def skill_on_off_switch(self, skill_num):
        if self.skills.earned == False:
            return
        current_time = time.time()
        if current_time - self.last_use_time >= self.cooltime:
           self.skills[skill_num].on = True

        else:
            self.skills[skill_num].on = False

    def skill_use(self,skill_num):
        if self.skills.earned == False:
            return
        if self.skills[skill_num].on:
            #common.effect.skill_effect_play(skill_num)
            self.last_use_time = time.time()
            self.skills[skill_num].on = False
            self.skills[skill_num].activate()
            common.hero.happy = min(100, common.hero.happy + 10)

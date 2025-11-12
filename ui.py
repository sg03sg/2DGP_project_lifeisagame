from pico2d import *
import game_framework

import play_mode

# 화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Ui:
    def __init__(self,name,x):
        if name == 'hp':
            self.image = load_image("hp_bar.png")
            self. percent = play_mode.hero.hp / 100
            self.kind = 0
        elif name == 'happy':
            self.image = load_image("happy_bar.png")
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

from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('spr_Babyroom_1.png')
        self.BG_WIDTH = self.image.w // 3
        self.BG_HEIGHT = self.image.h
        self.frame_count = 3
        self.offset = 0.0
        self.scroll_speed = 200  # 픽셀/초

    def update(self):
        # frame_time은 lifeisagame.py에서 delay(0.02)와 맞춤
        frame_time = 0.02
        self.offset += self.scroll_speed * frame_time
        self.offset %= (self.BG_WIDTH * self.frame_count)

    def draw(self):
        w = get_canvas_width()
        h = get_canvas_height()
        left = int(self.offset)
        x = - (left % self.BG_WIDTH)
        drawn_width = 0
        while drawn_width < w:
            frame_idx = (left // self.BG_WIDTH + drawn_width // self.BG_WIDTH) % self.frame_count
            sx = frame_idx * self.BG_WIDTH + (left % self.BG_WIDTH if drawn_width == 0 else 0)
            sw = min(self.BG_WIDTH - (left % self.BG_WIDTH) if drawn_width == 0 else self.BG_WIDTH, w - drawn_width)
            if sw <= 0:
                break
            dx = int(x + drawn_width + sw // 2)
            self.image.clip_draw(int(sx), 0, int(sw), self.BG_HEIGHT, dx, h // 2, int(sw), h)
            drawn_width += sw
            left += sw

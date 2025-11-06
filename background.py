from pico2d import *

# 화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Background:
    def __init__(self):
        self.image = load_image('spr_Babyroom_1.png')
        self.frame_count = 3
        self.frame_w = self.image.w // self.frame_count
        self.frame_h = self.image.h
        self.offset = 0.0
        self.scroll_speed = 40.0
        self.total_w = self.frame_w * self.frame_count

    def update(self):
        frame_time = 0.02
        self.offset += self.scroll_speed * frame_time

    def draw(self):
        ofs = int(self.offset) % self.total_w
        primary = (ofs // self.frame_w) % self.frame_count
        i = ofs % self.frame_w  # primary 프레임에서 잘려나간 픽셀 수(다음 프레임이 차지할 너비)

        # 스케일 : 원본 프레임 폭 -> 화면 폭
        scale_x = SCREEN_WIDTH / float(self.frame_w)

        # primary 부분
        primary_x = primary * self.frame_w + i
        primary_w = self.frame_w - i

        if primary_w > 0:
            primary_dest_w = int(primary_w * scale_x)
            # 중심 좌표 계산
            primary_center_x = primary_dest_w // 2
            self.image.clip_draw(primary_x, 0, primary_w, self.frame_h,
                                 primary_center_x, SCREEN_HEIGHT // 2,
                                 primary_dest_w, SCREEN_HEIGHT)

        # next 부분
        if i > 0:
            next_frame = (primary + 1) % self.frame_count
            next_src_x = next_frame * self.frame_w
            next_src_w = i
            next_dest_w = SCREEN_WIDTH - int((self.frame_w - i) * scale_x)
            # next의 중심 좌표
            next_center_x = (SCREEN_WIDTH - next_dest_w // 2)

            self.image.clip_draw(next_src_x, 0, next_src_w, self.frame_h,
                                 SCREEN_WIDTH - next_dest_w // 2, SCREEN_HEIGHT // 2,
                                 next_dest_w, SCREEN_HEIGHT)

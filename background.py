from pico2d import *
import game_framework
# 화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PIXEL_PER_METER = (10.0 / 1.7)  # 방 사진 크기/3 = 170 pixel = 약300 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# class bridge:
#     def __init__(self):
#         self.image = load_image('bridge.png')
#
#     def draw(self):
#         self.image.draw(self.x,self.y).

class Background:
    def __init__(self, filenames=None, loop=True):
        if filenames is None:
            filenames = ['Images/Babyroom.png','Images/childroom.png']
        self.images = [load_image(f) for f in filenames]
        self.frame_count = 3
        # 각 이미지의 프레임 폭/높이
        self.frame_w = [f.w // self.frame_count for f in self.images]
        self.frame_h = [f.h for f in self.images]
        # 각 이미지의 총 폭(프레임수 * 한 프레임 폭)
        self.total_w = [fw * self.frame_count for fw in self.frame_w]

        self.offset = 0.0
        self.scroll_speed = RUN_SPEED_PPS
        self.stage = 0
        self.loop = loop

    def update(self):
        self.offset += self.scroll_speed * game_framework.frame_time

        # 반복 모드: offset이 여러 스테이지를 그림
        if self.loop:
            while self.offset >= self.total_w[self.stage]:
                self.offset -= self.total_w[self.stage]
                self.stage = (self.stage + 1) % len(self.images)
        else:
            # 비반복 모드: 마지막 이미지에서 멈춤
            while self.stage < len(self.images) - 1 and self.offset >= self.total_w[self.stage]:
                self.offset -= self.total_w[self.stage]
                self.stage += 1
            if self.stage == len(self.images) - 1:
                self.offset = min(self.offset, self.total_w[self.stage] - 1)

    def draw(self):
        ofs = int(self.offset)
        fw = self.frame_w[self.stage]
        fh = self.frame_h[self.stage]

        # 현재 프레임에서 잘린 픽셀 수 = i
        primary = ofs // fw
        i = ofs % fw
        primary_frame = int(primary % self.frame_count)

        # 한 프레임을 화면 폭으로 스케일
        scale_x = SCREEN_WIDTH / float(fw)

        # 현재 프레임 그리기
        primary_src_x = primary_frame * fw + i
        primary_src_w = fw - i

        if primary_src_w > 0:
            primary_dest_w = int(primary_src_w * scale_x)
            self.images[self.stage].clip_draw(primary_src_x, 0, primary_src_w, fh,
                                              primary_dest_w // 2, SCREEN_HEIGHT // 2,
                                              primary_dest_w, SCREEN_HEIGHT)
        else:
            primary_dest_w = 0

        # 다음 부분이 필요하면 그리기
        if i > 0:
            # 다음 프레임이 같은 스테이지에 있는지, 다음 이미지의 첫 프레임인지 검사
            if primary_frame < self.frame_count - 1:
                next_stage = self.stage
                next_frame_idx = primary_frame + 1
            else:
                next_stage = (self.stage + 1) % len(self.images)
                next_frame_idx = 0

            next_src_x = next_frame_idx * fw
            next_src_w = i

            # 남은 화면 폭을 next로 채움
            next_dest_w = SCREEN_WIDTH - primary_dest_w
            if next_dest_w > 0 and next_src_w > 0:
                self.images[next_stage].clip_draw(next_src_x, 0, next_src_w, fh,
                                                  primary_dest_w + next_dest_w // 2, SCREEN_HEIGHT // 2,
                                                  next_dest_w, SCREEN_HEIGHT)

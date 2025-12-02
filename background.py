from pico2d import *
import game_framework
import play_mode
import gate
import game_world

import itertools


# 화면 크기
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PIXEL_PER_METER = (10.0 / 1.7)  # 방 사진 크기/3 = 170 pixel = 약300 cm
RUN_SPEED_KMPH = 22.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) *2

# 아래쪽을 얼마나 띄울지(바닥 여유) - 필요시 조절
BOTTOM_OFFSET = 100

def screen_speed(frame_width):
    scale_x = SCREEN_WIDTH / float(frame_width)
    return RUN_SPEED_PPS * scale_x

class Background:
    def __init__(self, filenames=None, loop=True):
        if filenames is None:
            filenames = ['Images/Babyroom_demo.png','Images/childroom.png','Images/hobby_map.png', 'Images/student_map.png']
        self.images = [load_image(f) for f in filenames]
        # 각 이미지 별 프레임 수(픽셀 170으로 분할한 값)와 그에 따른 폭/높이/총폭을 각각 계산
        self.frame_count = [img.w // 170 if img.w >= 170 else 1 for img in self.images]
        self.frame_w = [img.w // cnt if cnt > 0 else img.w for img, cnt in zip(self.images, self.frame_count)]
        self.frame_h = [img.h for img in self.images]
        self.total_w = [fw * cnt for fw, cnt in zip(self.frame_w, self.frame_count)]
        self.map_total_w = list(itertools.accumulate(self.total_w))
        self.stage = 0
        self.logic_stage_age = [0, 1, 2, 2, 2]

        self.offset = 0.0
        self.scroll_speed = RUN_SPEED_PPS
        self.loop = loop
        self.hero_pos = self.frame_w[self.stage] * 0.5
        self.total_run = 0

        self.gate_pos = [total_pos - end_frame  for total_pos,end_frame in zip(self.map_total_w, self.frame_w)]
        self.gate = []
        self.gate_exist = [False for _ in range(len(self.images))]

        self.base_scale = SCREEN_WIDTH / float(self.frame_w[0])
        self.display_speed = RUN_SPEED_PPS * self.base_scale  # 화면상에서 고정된 픽셀/초 속도

        self.hero_stage =0

    def update(self):
        scale = SCREEN_WIDTH / float(self.frame_w[self.stage])
        # 화면 기준 고정 속도(display_speed)를 원본 픽셀(offset) 단위로 변환
        src_speed = self.display_speed / scale

        self.offset += src_speed * game_framework.frame_time
        self.hero_pos += src_speed * game_framework.frame_time
        self.total_run += src_speed * game_framework.frame_time

        self.gate_make()

        if self.hero_pos >= self.total_w[self.stage]:
            self.gate[0].frame_move = True
            self.hero_pos = 0
            self.hero_stage = (self.hero_stage+1) % len(self.images)
            next_stage = (self.stage + 1) % len(self.images)
            if self.logic_stage_age[self.stage] != self.logic_stage_age[next_stage]:
                play_mode.hero.age = (play_mode.hero.age+1) % 3
            if not play_mode.hero.state_machine.cur_state == play_mode.hero.jump:
                play_mode.hero.y = 150 + int((play_mode.hero.tall[play_mode.hero.age]-100)//2)
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

    def gate_make(self):
        for i, g_pos in enumerate(self.gate_pos):
            if g_pos <= self.total_run and self.total_run <= self.map_total_w[i] + float(gate.gate_size / 2) and not self.gate_exist[i]:
                if i == 0:
                    # if g_pos <= self.total_run and self.total_run <= self.map_total_w[i]+55:
                    #     if not self.gate_exist[i]:
                    self.gate_exist[i] = True
                    new_gate= gate.Door()
                    self.gate.append(new_gate)
                    game_world.add_object(self.gate[i],2)

                else:
                    self.gate_exist[i] = True
                    new_gate = gate.Gate()
                    self.gate.append(new_gate)
                    game_world.add_object(self.gate[i],2)


    def draw(self):
        ofs = int(self.offset)
        fw = self.frame_w[self.stage]
        fh = self.frame_h[self.stage]

        # 현재 프레임에서 잘린 픽셀 수 = i
        primary = ofs // fw
        i = ofs % fw
        primary_frame = int(primary % self.frame_count[self.stage])

        # 한 프레임을 화면 폭으로 스케일
        scale_x = SCREEN_WIDTH / float(fw)
        scale_y = (SCREEN_HEIGHT  - BOTTOM_OFFSET) / float(fh)

        # 현재 프레임 그리기
        primary_src_x = primary_frame * fw + i
        primary_src_w = fw - i

        if primary_src_w > 0:
            primary_dest_w = int(primary_src_w * scale_x)
            primary_dest_h = int(fh*scale_y)
            self.images[self.stage].clip_draw(primary_src_x, 0, primary_src_w, fh,
                                              primary_dest_w // 2, primary_dest_h // 2 + BOTTOM_OFFSET ,
                                              primary_dest_w, primary_dest_h)
        else:
            primary_dest_w = 0

        # 다음 부분이 필요하면 그리기
        if i > 0:
            # 다음 프레임이 같은 스테이지에 있는지, 다음 이미지의 첫 프레임인지 검사
            if primary_frame < self.frame_count[self.stage] - 1:
                next_stage = self.stage
                next_frame_idx = primary_frame + 1
            else:
                next_stage = (self.stage + 1) % len(self.images)
                next_frame_idx = 0

            next_fw = self.frame_w[next_stage]
            next_fh = self.frame_h[next_stage]
            next_src_x = next_frame_idx * next_fw
            next_src_w = i

            scale_next_x = SCREEN_WIDTH / float(next_fw)
            scale_next_y = (SCREEN_HEIGHT - BOTTOM_OFFSET) / float(next_fh)

            # 남은 화면 폭을 next로 채움
            next_dest_w = SCREEN_WIDTH - primary_dest_w
            next_dest_h = int(next_fh * scale_next_y)
            if next_dest_w > 0 and next_src_w > 0:
                self.images[next_stage].clip_draw(next_src_x, 0, next_src_w, next_fh,
                                                  primary_dest_w + next_dest_w // 2, next_dest_h // 2 + BOTTOM_OFFSET,
                                                  next_dest_w, next_dest_h)


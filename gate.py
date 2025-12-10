from pico2d import *
import game_framework
import game_world
import common

with open('Json/door_data.json', 'r', encoding='utf-8') as f:
    door_rounding_box_data = json.load(f)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_OFFSET = 100

#문 속도
TIME_PER_ACTION = 0.5 #문을 박차고 나갈때 열리는 평균 시간은 약 0.5초
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

gate_size = 30

class Door:
    def __init__(self):
        self.image = load_image('Images/door.png')
        self.frame = 0
        self.size = [10, 25, 40, 45]
        self.x = 1310
        self.y = SCREEN_HEIGHT // 2 + BOTTOM_OFFSET // 2
        self.frame_move = False

        self.door_sound = load_wav('Sound/16_sfx_Door.wav')
        self.door_sound.set_volume(40)
        self.sound_play = False

    def update(self):
        self.x -= common.background.display_speed * game_framework.frame_time
        if self.x < - 55:
            game_world.remove_object(self)

        if self.frame_move:
            if not self.sound_play:
                self.door_sound.play()
                self.sound_play = True
            self.frame = self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time
            if self.frame > 3:
                self.frame = 3
                self.frame_move = False

    def draw(self):
        i = int(self.frame)
        self.image.clip_draw(int(door_rounding_box_data['sprites'][i]["x"]),
                             int(door_rounding_box_data['sprites'][i]['y']),
                             int(door_rounding_box_data['sprites'][i]['width']),
                             int(door_rounding_box_data['sprites'][i]['height']),
                             self.x + self.size[int(self.frame)] // 2, self.y, 60 + self.size[i],
                             SCREEN_HEIGHT - BOTTOM_OFFSET)


class Gate:
    def __init__(self):
        self.image = load_image('Images/gate_out.png')
        self.size = gate_size
        self.x = 1317
        self.y = SCREEN_HEIGHT // 2 + BOTTOM_OFFSET // 2

    def update(self):
        self.x -= common.background.display_speed * game_framework.frame_time
        if self.x < - float((60 + self.size)/2):
            game_world.remove_object(self)

    def draw(self):
        self.image.clip_draw(0,0,91,260,self.x, self.y, 60 + self.size, SCREEN_HEIGHT - BOTTOM_OFFSET)
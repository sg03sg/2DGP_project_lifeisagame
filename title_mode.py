from pico2d import *
import game_framework
import play_mode

title = None

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_OFFSET = 0

with open('Json/title_logo_data.json', 'r', encoding='utf-8') as f:
    l = json.load(f)
logo_title_data = l['sprites']

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 /TIME_PER_ACTION
FRAMES_PER_ACTION = 7

class Title:
    def __init__(self):
        self.image = load_image('Images/baby_map.png')
        self.baby_img = load_image('Images/baby_sprite_sheet.png')
        self.title_logo_img = load_image('Images/title_logo.png')
        self.title_message_img = load_image('Images/title_button.png')
        self.frame_w = 320
        self.frame_h = self.image.h
        self.frame = 0
        self.bgm = load_music('Sound/02_bgm_Start.wav')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 7

    def draw(self):
        ##아기
        self.baby_img.draw(640, 50+BOTTOM_OFFSET,100,100)
        ##배경
        sh = SCREEN_HEIGHT - BOTTOM_OFFSET
        scale_y = (SCREEN_HEIGHT  - BOTTOM_OFFSET) / float(self.frame_h)
        y = self.frame_h *scale_y //2 + BOTTOM_OFFSET
        self.image.clip_draw(0,0, self.frame_w,self.frame_h, SCREEN_WIDTH//2, y,SCREEN_WIDTH,SCREEN_HEIGHT  - BOTTOM_OFFSET)
        ##로고,버튼
        if not start_game:
            i = int(self.frame)
            frame_data = logo_title_data[i]
            ##로고
            self.title_logo_img.clip_draw(int(frame_data["x"]),int(frame_data["y"]),int(frame_data["width"]),int(frame_data["height"]),
                                          SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100,500,200)
            ##버튼
            self.title_message_img.draw( SCREEN_WIDTH//2, 150,400,50)


def init():
    global title, black_img, start_game
    black_img = load_image('Images/black.png')
    start_game = False
    title = Title()

def finish():
    global title
    del title
def handle_events():
    global start_game
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            start_game = True


def draw():
    clear_canvas()
    black_img.draw(640,360,1280,720)
    title.draw()
    update_canvas()

def update():
    global BOTTOM_OFFSET, start_game

    title.update()

    if not start_game:
        return

    # 0.5초에 걸쳐 100으로
    # 속도 = 거리 / 시간 = 100 / 0.5 = 200 px/sec
    BOTTOM_OFFSET += 200 * game_framework.frame_time

    if BOTTOM_OFFSET >= 100:
        BOTTOM_OFFSET = 100
        game_framework.change_mode(play_mode)
def pause(): pass
def resume(): pass
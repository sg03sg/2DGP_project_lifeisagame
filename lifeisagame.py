from pico2d import *
import random


# Game object class here

class Background:
    def __init__(self):
        # 이미지가 resource 폴더에 있으므로 경로를 수정
        self.image = load_image('resource/spr_Babyroom_1.png')

    def draw(self):
        # 캔버스 크기에 맞게 중앙에 스케일하여 그리기
        w = get_canvas_width()
        h = get_canvas_height()
        self.image.draw(w // 2, h // 2, w, h)

    def update(self):
        pass


class hero:
    def __init__(self):
        self.x, self.y = 640, 150
        self.frame = -1
        self.y_frame =-1
        self.face_dir = 1
        self.image = load_image('nobaby.png')

    def update(self):
        self.frame = (self.frame + 1) % 10
        if self.frame % 10 == 0:
            self.y_frame = (self.y_frame +1) % 3
        pass

    def draw(self):
        if self.face_dir == 1:
          self.image.clip_composite_draw(self.frame * 153, 323-self.y_frame*113, 120, 90,0,'h', self.x, self.y,100,100)
        # else:
        #     self.image.clip_draw(self.frame * 100, 200, 100, 100, self.x, self.y)
        pass


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global world
    global boy

    world = []

    background = Background()
    world.append(background)

    boy = hero()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas(1280,720)
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.02)
# finalization code
close_canvas()

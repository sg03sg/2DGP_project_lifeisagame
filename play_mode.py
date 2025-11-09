from pico2d import *
from background import Background
from hero import Hero
import game_world

running = True

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            hero.handle_event(event)


def init():
    global world
    global hero

    running = True
    background = Background()
    game_world.add_object(background,0)

    hero = Hero()
    game_world.add_object(hero,1)



def update_world():
    game_world.update()


def draw():
    clear_canvas()
    game_world.draw()
    update_canvas()

def finish():
    pass

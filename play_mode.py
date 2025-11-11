from pico2d import *

from background import Background
from hero import Hero

import game_world
import game_framework


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            hero.handle_event(event)


def init():
    global hero
    global running

    background = Background()
    game_world.add_object(background,0)

    hero = Hero()
    game_world.add_object(hero,1)



def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.draw()
    update_canvas()

def finish():
    game_world.clear()

def pauese():
    pass
def resume():
    pass

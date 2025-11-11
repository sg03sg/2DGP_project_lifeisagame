from pico2d import *
import random

from background import Background
from hero import Hero
from item import Item

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
    global background

    global running

    background = Background()
    game_world.add_object(background,0)

    hero = Hero()
    game_world.add_object(hero,1)

def update():
    global item
    item_timer = game_framework.game_time
    if int(item_timer) % 2 == 0:
        if not any(isinstance(obj, Item) for obj in game_world.world[1]):
            item_y = 150 + 200 * (random.randint(0, 1))
            item = Item(item_y)
            game_world.add_object(item, 1)
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

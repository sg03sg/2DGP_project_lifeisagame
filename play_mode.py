from pico2d import *
import random

from background import Background
from hero import Hero
from item_spawner import ItemSpawner
from item import Item
from ui import Ui, Skillui, Ageui

import game_world
import game_framework
import savelist
import common


item_spawner = None
black_img = None
ageui = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            common.hero.handle_event(event)

def init():
    global black_img, item_spawner, ageui

    common.background = Background()
    game_world.add_object(common.background, 0)

    common.hero = Hero()
    game_world.add_object(common.hero, 1)

    ageui = Ageui(common.hero.age)

    skills = [Skillui(i) for i in savelist.skillname]
    game_world.add_objects(skills, 1)

    hp = Ui("hp", 50)
    game_world.add_object(hp, 1)
    happy = Ui("happy", 250)
    game_world.add_object(happy, 1)

    black_img = load_image('Images/black.png')

    # 기존 충돌 설정 유지
    game_world.add_collision_pair('hero:item', common.hero, None)

    item_spawner = ItemSpawner(init_spawn_interval=1.5)

def update():
    global ageui, item_spawner

    ageui.update(common.hero.age)
    item_spawner.update(common.hero,common.background)

    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    if black_img:
        black_img.draw(get_canvas_width()//2, get_canvas_height()//2,
                       get_canvas_width(), get_canvas_height())
    ageui.draw()
    game_world.draw()
    update_canvas()

def finish():
    global item_spawner
    if item_spawner:
        item_spawner.clear()
    game_world.clear()

def pause():
    pass

def resume():
    pass
from pico2d import *
import random

from background import Background
from hero import Hero
from item_spawner import ItemSpawner
from item import Item
from ui import Ui, Skillui, Age1ui

import game_world
import game_framework
from savelist import Itemlist, Uilist

background = None
hero = None
itemlist = Itemlist()
uilist = Uilist()
item_spawner = None

black_img = None
age1uis = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            hero.handle_event(event)

def init():
    global hero, background, black_img, item_spawner

    background = Background()
    game_world.add_object(background, 0)

    hero = Hero()
    game_world.add_object(hero, 1)

    skills = [Skillui(i) for i in uilist.skillname]
    game_world.add_objects(skills, 1)

    hp = Ui("hp", 50)
    game_world.add_object(hp, 1)
    happy = Ui("happy", 250)
    game_world.add_object(happy, 1)

    black_img = load_image('Images/black.png')

    # 기존 충돌 설정 유지
    game_world.add_collision_pair('hero:item', hero, None)

    item_spawner = ItemSpawner(itemlist, init_spawn_interval=1.5)

def update():
    global age1uis, hero, item_spawner

    # 기존 나이 UI 로직 그대로 유지
    if hero.age == 1:
        if not age1uis:
            age1uis = [Age1ui(i) for i in uilist.age1uiname]
            game_world.add_objects(age1uis, 1)
    else:
        if age1uis:
            for ui in age1uis:
                try:
                    game_world.remove_object(ui)
                except ValueError:
                    pass
            age1uis = None

    item_spawner.update(hero,background)

    game_world.update()
    game_world.handle_collisions()

def draw():
    clear_canvas()
    if black_img:
        black_img.draw(get_canvas_width()//2, get_canvas_height()//2,
                       get_canvas_width(), get_canvas_height())
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
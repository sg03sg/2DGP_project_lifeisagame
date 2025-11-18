from pico2d import *
import random

from background import Background
from hero import Hero
from item import Item
from ui import Ui

import game_world
import game_framework

background = None
hero = None

item_pos = [[150,350],[570]]

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

    global hp
    global happy

    global running

    global black_img

    global item_last_age,item_list
    item_list = []
    item_last_age = 0

    global itemspawn_timer, item_last_spawn
    itemspawn_timer = 1.5
    item_last_spawn = game_framework.game_time

    background = Background()
    game_world.add_object(background,0)

    hero = Hero()
    game_world.add_object(hero,1)

    hp= Ui("hp",50)
    game_world.add_object(hp,1)
    happy= Ui("happy",250)
    game_world.add_object(happy,1)

    game_world.add_collision_pair('hero:item', hero, None)
    black_img = load_image('Images/black.png')



def update():
    global item
    global hero

    global itemspawn_timer, item_last_spawn
    global item_pos

    global item_last_age,item_list

    if hero.age > item_last_age:
        removes = [remove for remove in item_list if remove.age < hero.age]
        for remove in removes:
            game_world.remove_object(remove)
            item_list.remove(remove)
        item_last_age = hero.age

    now = game_framework.game_time
    if now - item_last_spawn >= itemspawn_timer:
        # if not any(isinstance(obj, Item) for obj in game_world.world[1]):
        item_y = random.choice(item_pos[hero.age])
        item = Item(None,item_y, hero.age)
        game_world.add_object(item, 1)
        game_world.add_collision_pair('hero:item', None, item)
        item_list.append(item)
        item_last_spawn = now

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
    game_world.clear()

def pauese():
    pass
def resume():
    pass

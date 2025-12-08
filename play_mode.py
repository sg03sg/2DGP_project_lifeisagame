from pico2d import *
import random

from background import Background
from hero import Hero
from item_spawner import ItemSpawner
from job_system import Job_select
from pause import Pause_test
from item import Item
from select_system import Select_System
from ui import Ui, Skillui, Ageui, Money_ui

import game_world
import game_framework
import savelist
import common


black_img = None
ageui = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_TAB:
            if not common.selecting:
                common.select_system.select_state = True
        else:
            common.hero.handle_event(event)

def init():
    global black_img, ageui

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
    money = Money_ui("coin")
    game_world.add_object(money, 1)

    black_img = load_image('Images/black.png')
    common.job_select = Job_select()
    common.pause_test = Pause_test(common.pause_def)

    common.select_system = Select_System()
    game_world.add_object(common.select_system, 0)

    # 기존 충돌 설정 유지
    game_world.add_collision_pair('hero:item', common.hero, None)

    common.item_spawner = ItemSpawner(init_spawn_interval=1.5)

def update():
    global ageui

    ageui.update(common.hero.age)

    common.item_spawner.update(common.hero)
    game_world.update()
    game_world.handle_collisions()

    if common.pause_test.do_select_job:
        import select_job_mode
        game_framework.push_mode(select_job_mode)
        return

def draw():
    clear_canvas()
    if black_img:
        black_img.draw(get_canvas_width()//2, get_canvas_height()//2,
                       get_canvas_width(), get_canvas_height())
    ageui.draw()
    game_world.draw()
    update_canvas()

def draw_another_mode():
    if black_img:
        black_img.draw(get_canvas_width()//2, get_canvas_height()//2,
                       get_canvas_width(), get_canvas_height())
    ageui.draw()
    game_world.draw()


def finish():
    if common.item_spawner:
        common.item_spawner.clear()
    game_world.clear()

def pause():
    pass

def resume():
    pass
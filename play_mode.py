from pico2d import *

from background import Background
from ending_system import Ending_system
from hero import Hero
from item_spawner import ItemSpawner
from job_system import Job_select,Job_stat
from pause import Pause_test
from select_system import Select_System
from skill_system import Skill_system
from ui import Ui, Skillui, Ageui, Money_ui
from effect import Effect

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_o:
            if common. draw_rec:
                common.draw_rec = False
            else:
                common.draw_rec = True
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            if common.using_skill:
                continue  # 스킬 사용 중일 때는 무시
            mx, my = event.x, get_canvas_height() - event.y  # 마우스 좌표

            # 스킬 버튼들 검사
            for idx, skill in enumerate(common.skills):
                half = skill.size / 2
                left = skill.x - half
                right = skill.x + half
                bottom = skill.y - half
                top = skill.y + half

                if left <= mx <= right and bottom <= my <= top:
                    common.skill_system.skill_use(idx)
                    print('click')
                    break
        else:
            common.hero.handle_event(event)

def init():
    global black_img, ageui

    common.background = Background()
    game_world.add_object(common.background, 0)

    common.hero = Hero()
    game_world.add_object(common.hero, 1)

    ageui = Ageui(common.hero.age)

    common.skills = [Skillui(i) for i in savelist.skillname]
    game_world.add_objects(common.skills, 1)

    common.skill_system = Skill_system()
    common.ending_system = Ending_system()
    common.job_stat = Job_stat()
    common.propose_probality = 50
    common.friend_probality = 80
    common.selecting = False
    common.using_skill = False
    common.effect = Effect()
    draw_rec = False

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
    common.skill_system.update()
    common.ending_system.update()

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
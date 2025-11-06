from pico2d import *

from background import Background
from hero import Hero

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


def reset_world():
    global world
    global hero

    world = []

    background = Background()
    world.append(background)

    hero = Hero()
    world.append(hero)



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
    delay(0.08)
# finalization code
close_canvas()

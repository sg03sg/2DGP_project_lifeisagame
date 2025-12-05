from pico2d import *
import game_framework
import common
import play_mode

def init():
    common.pause_def.pause_game_switch()  # 배경/캐릭터/아이템 stop = freeze

# 방향키/스페이스로 직업 선택
def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_TAB:
            common.job_select.get_job()

def update():
    common.job_select.update()

def draw():
    play_mode.draw()  # 아래에 정지된 화면 그대로 그린다
    common.job_select.draw()  # 그 위에 UI overlay

def finish():
    common.pause_def.resume_game_switch()  # 게임 재개
    common.hero.age = 3  # 직업 선택 모드 종료 후 age 변경

def pause(): pass

def resume(): pass
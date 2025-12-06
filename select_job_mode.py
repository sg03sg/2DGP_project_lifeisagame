from pico2d import *
import game_framework
import common
import play_mode
import itertools

def init():
    common.pause_def.pause_game_switch()  # 배경/캐릭터/아이템 stop = freeze


##캐릭터의 직업별 생김새 추가 함수
def apply_job_resources(job_num):
    job_data = {
        0: {
            "walk_img": ['Images/no_job_run.png', 'Images/middle_no_job_run.png'],
            "jump_img": ['Images/no_job_jump.png', 'Images/middle_no_job_jump.png'],
            "walk_json": ['Json/no_job_run_data.json', 'Json/middle_no_job_run_data.json'],
            "jump_json": ['Json/no_job_jump_data.json', 'Json/middle_no_job_jump_data.json'],
        },
        1: {
            "walk_img": ['Images/officer_run.png', 'Images/middle_officer_run.png'],
            "jump_img": ['Images/officer_jump.png', 'Images/middle_officer_jump.png'],
            "walk_json": ['Json/officer_run_data.json', 'Json/middle_officer_run_data.json'],
            "jump_json": ['Json/officer_jump_data.json', 'Json/middle_officer_jump_data.json'],
        },
        2: {
            "walk_img": ['Images/art_run.png', 'Images/middle_art_run.png'],
            "jump_img": ['Images/art_jump.png', 'Images/middle_art_jump.png'],
            "walk_json": ['Json/art_run_data.json', 'Json/middle_art_run_data.json'],
            "jump_json": ['Json/art_jump_data.json', 'Json/middle_art_jump_data.json'],
        },
        3: {
            "walk_img": ['Images/musician_run.png', 'Images/middle_musician_run.png'],
            "jump_img": ['Images/musician_jump.png', 'Images/middle_musician_jump.png'],
            "walk_json": ['Json/musician_run_data.json', 'Json/middle_musician_run_data.json'],
            "jump_json": ['Json/musician_jump_data.json', 'Json/middle_musician_jump_data.json'],
        },
        4: {
            "walk_img": ['Images/soccer_run.png', 'Images/middle_soccer_run.png'],
            "jump_img": ['Images/soccer_jump.png', 'Images/middle_soccer_jump.png'],
            "walk_json": ['Json/soccer_run_data.json', 'Json/middle_soccer_run_data.json'],
            "jump_json": ['Json/soccer_jump_data.json', 'Json/middle_soccer_jump_data.json'],
        },
    }

    info = job_data[job_num]

    hero = common.hero

    # Hero 이미지 등록
    for fn in range(2):
        hero.walk_images.append(load_image(info["walk_img"][fn]))
        hero.jump_images.append(load_image(info["jump_img"][fn]))

    # JSON 데이터 등록
    import json
    import hero as h
    for fn in range(2):
        with open(info["walk_json"][fn], 'r', encoding='utf-8') as f:
            h.hero_rounding_box_data.append(json.load(f))

        with open(info["jump_json"][fn], 'r', encoding='utf-8') as f:
            h.hero_jump_rounding_box_data.append(json.load(f))

    h.scale_hero_def(h.scale_hero)

    bg = common.background
    bg.map_total_w = list(itertools.accumulate(bg.total_w[i] for i in bg.stage_order))
    bg.gate_pos = [total - bg.frame_w[i] for i, total in zip(bg.stage_order, bg.map_total_w)]

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
    clear_canvas()
    play_mode.draw_another_mode()  # 아래에 정지된 화면 그대로 그린다
    common.job_select.draw()  # 그 위에 UI overlay
    update_canvas()

def finish():
    job = common.hero.job  # 0~4

    if job == 0: # 무직
        common.background.stage_order += [5,4,11,12,13,5,13]
    elif job == 1:  # 직장인
        common.background.stage_order += [6,4,11,12,13,6,13]
    elif job == 2:  # 화가
        common.background.stage_order += [7,4,11,12,13,7,13]
    elif job == 3:  # 음악가
        common.background.stage_order += [8,4,11,12,13,8,13]
    elif job == 4:  # 축구선수
        common.background.stage_order += [9,4,11,12,13,9,13]

    apply_job_resources(job)

    common.pause_def.resume_game_switch()  # 게임 재개
    common.pause_test.do_select_job = False
    common.hero.age = 3  # 직업 선택 모드 종료 후 age 변경

def pause(): pass

def resume(): pass
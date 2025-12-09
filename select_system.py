from pico2d import *
import common
import game_framework
import game_world
import common
import json
import itertools
import savelist
import random

with open('Json/hobby_select_data.json', 'r', encoding='utf-8') as f:
    h = json.load(f)
with open('Json/flower_shop_select_data.json', 'r', encoding='utf-8') as f:
    flower = json.load(f)
with open('Json/hosue_shop_select_data.json', 'r', encoding='utf-8') as f:
    house = json.load(f)
with open('Json/propose_woman_data.json', 'r', encoding='utf-8') as f:
    propose = json.load(f)

with open('Json/sell_house_data.json', 'r', encoding='utf-8') as f:
    sell_h = json.load(f)

hobby_select_data = h['sprites']
flower_shop_select_data = flower['sprites']
house_shop_select_data = house['sprites']
propose_woman_data = propose['sprites']
sell_house_data = sell_h['sprites']

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BOTTOM_OFFSET = 100

select_offset = 2

def apply_old_resources(poor_power):
    if poor_power == 0:
        return  # 빈곤은 기본값이므로 패스
    job_data = {
        3: {
            "walk_img": 'Images/poor_old.png',
            "walk_json": 'Json/poor_old_data.json'
        },
        2: {
            "walk_img": 'Images/normal_old.png',
            "walk_json": 'Json/normal_old_data.json'
        },
        1: {
            "walk_img": 'Images/rich_old.png',
            "walk_json": 'Json/rich_old_data.json'
        }
    }

    info = job_data[poor_power]

    hero = common.hero

    hero.walk_images.pop(len(hero.walk_images)-1)
    hero.jump_images.pop(len(hero.jump_images)-1)

    # Hero 이미지 등록
    hero.walk_images.append(load_image(info["walk_img"]))
    hero.jump_images.append(load_image(info["walk_img"]))

    # JSON 데이터 등록
    import json
    import hero as h
    h.hero_rounding_box_data.pop(len(h.hero_rounding_box_data)-1)
    h.hero_jump_rounding_box_data.pop(len(h.hero_jump_rounding_box_data)-1)
    with open(info["walk_json"], 'r', encoding='utf-8') as f:
        h.hero_rounding_box_data.append(json.load(f))

    with open(info["walk_json"], 'r', encoding='utf-8') as f:
        h.hero_jump_rounding_box_data.append(json.load(f))

    h.scale_hero_def(h.scale_hero)

    bg = common.background
    for _ in range(2):
        bg.stage_order.pop(len(bg.stage_order)-1)
    if poor_power == 3:
        bg.stage_order += [16,17]
    elif poor_power == 2:
        bg.stage_order += [17, 19]
    elif poor_power == 1:
        bg.stage_order += [18, 19]

    bg.map_total_w = list(itertools.accumulate(bg.total_w[i] for i in bg.stage_order))
    bg.gate_pos = [total - bg.frame_w[i] for i, total in zip(bg.stage_order, bg.map_total_w)]

##선택 시스템 객체 게임월드에 추가를 결정하는 함수1
##Tab을 눌렀을때 선택 상태를 활성화 상태로 만든다 함수 2
class Select_System:
    def __init__(self):
        self.selects = [Hobby(0),Hobby(1),Hobby(2), Flower_shop(0),Flower_shop(1),Flower_shop(2),Flower_shop(3), House_shop(0),House_shop(1),House_shop(2),House_shop(3),Propose(0),Friend()]
        self.select_state = False

    def select_decision(self,other):
        background = common.background
        pos = other.pos
        if pos <= background.total_run and not other.exist: # <= self.map_total_w[self.stage] + float(gate.gate_size / 2)
            other.exist = True
            game_world.add_object(other, 0)

    def handle_select(self):
        if not self.select_state:
            return

        hero_x = common.hero.x
        min_dist = 999999
        selected_obj = None

        for obj in self.selects:
            if not obj.exist:
                continue
            if not obj.handle_collision(common.hero):
                continue
            if not obj.can_select:
                continue

            # X 좌표 거리만 체크 (러닝게임 특성상 충분)
            dist = abs(obj.x - hero_x)

            if dist < min_dist:
                min_dist = dist
                selected_obj = obj

        if selected_obj:
            selected_type = type(selected_obj)
            for obj in self.selects:
                if isinstance(obj, selected_type):
                    obj.can_select = False  # 같은 타입은 선택 불가
            selected_obj.selected = True
            print("선택 객체:", selected_obj)

        self.select_state = False  # 선택 후 종료


    def update(self):
        for select in self.selects:
            self.select_decision(select)
        self.handle_select()
    def draw(self):
        pass

##동아리 선택 객체를 그리고 충돌 범위를 저장
class Hobby:
    def __init__(self,num = 0):
        self.image = load_image('Images/hobby_select.png')
        self.w = hobby_select_data[num]['width'] * 2
        self.h = hobby_select_data[num]['height'] * 2
        self.x = 1310
        self.y = common.hero.y - 20
        self.num = num
        self.pos = common.background.map_total_w[1] - common.background.frame_w[1] + 80 * (num+1)
        self.exist = False
        self.selected = False
        self.can_select = True

        self.choice_img = load_image('Images/choice_ui.png')

    def handle_collision(self,other):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def hobby_happy(self):
        if self.num == 0:
            savelist.item_stats['paint']['happy'] = + 5
        elif self.num == 1:
            savelist.item_stats['music']['happy'] = + 5
        elif self.num == 2:
            savelist.item_stats['soccer']['happy'] = + 5

    def select_collision(self):
        if self.selected:
            common.selecting = True
            common.hobby_num = self.num
            common.skills[0].skill_earn = True
            self.hobby_happy()
            common.hero.earn_hobby.num = self.num
            common.hero.state_machine.handle_state_event(('select',None))
            common.pause_def.pause_game_switch()
            self.selected = False
        else:
            return

    def get_bb(self):
        half_w = self.w // 2
        half_h = self.h // 2
        return self.x - half_w - select_offset, self.y , self.x + half_w+select_offset, self.y + self.h

    def update(self):
        self.x -= common.background.display_speed * game_framework.frame_time
        self.select_collision()
        if self.x < - 55:
            self.exist = False
            game_world.remove_object(self)

    def draw(self):
        i = self.num
        w = self.w
        h = self.h
        self.choice_img.draw(self.x, self.y + self.h //2 + 40+ h//2, 150, 50)
        self.image.clip_draw(int(hobby_select_data[i]["x"]),
                             int(hobby_select_data[i]['y']),
                             int(hobby_select_data[i]['width']),
                             int(hobby_select_data[i]['height']),
                             self.x, self.y + self.h //2, w, h)
        draw_rectangle(*self.get_bb())


class Flower_shop:
    def __init__(self,num = 0):
        self.image = load_image('Images/flower_shop_select.png')
        self.w = flower_shop_select_data[num]['width'] * 2
        self.h = flower_shop_select_data[num]['height'] * 2
        self.x = 1310
        self.y = SCREEN_HEIGHT // 2 + BOTTOM_OFFSET // 2 - 100
        self.num = num
        self.pos = common.background.map_total_w[10] ## 아무값이나 넣어놓기
        self.exist = False
        self.selected = False
        self.can_select = True
        self.money = [300,10]
        self.choice_img = load_image('Images/choice_ui.png')

    def handle_collision(self, other):
        if self.num in (0,2):
            return False
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def select_collision(self):
        if self.selected:
            common.selecting = True
            common.propose_probality = 50 + 10 * (self.num+1)
            num = 0 if self.num ==1 else 1
            if self.money[num] <= common.hero.money:
                print(2)
                common.hero.money -= self.money[num]
            common.selecting = False
            self.selected = False
            game_world.remove_object(self)
        else:
            return

    def get_bb(self):
        if self.num in (1,3):
            half_w = flower_shop_select_data[0]['width']
            flower_w = flower_shop_select_data[1]['width'] * 2
            return self.x - half_w - select_offset, BOTTOM_OFFSET, self.x + half_w + select_offset + flower_w, SCREEN_HEIGHT
        else:
            return 0, 0, 0, 0

    def update(self):
        self.select_collision()
        self.x -= common.background.display_speed * game_framework.frame_time
        if self.x < - 55:
            self.exist = False
            game_world.remove_object(self)

    def draw(self):
        i = self.num
        w = self.w
        h = self.h
        self.image.clip_draw(int(flower_shop_select_data[i]["x"]),
                             int(flower_shop_select_data[i]['y']),
                             int(flower_shop_select_data[i]['width']),
                             int(flower_shop_select_data[i]['height']),
                             self.x, self.y + self.h //2, w, h)
        if self.num in (1,3):
            self.choice_img.draw(self.x, self.y + self.h // 2 + 40 + h // 2, 150, 50)
            draw_rectangle(*self.get_bb())

class House_shop:
    def __init__(self,num = 0):
        self.image = load_image('Images/house_shop_select.png')
        self.buy_house_image = load_image('Images/sell_house.png')
        if num == 0:
            self.w = house_shop_select_data[num]['width'] * 3
            self.h = house_shop_select_data[num]['height'] * 3
            self.y = common.hero.y
        else:
            self.w = house_shop_select_data[num]['width'] * 2
            self.h = house_shop_select_data[num]['height'] * 2
            self.y = common.hero.y - 20
        self.x = 1310
        self.num = num
        self.pos = common.background.map_total_w[10] ## 아무값이나 넣어놓기
        self.exist = False
        self.selected = False
        self.can_select = True
        self.buy = False
        self.money = [2000,1000, 0]

        self.choice_img = load_image('Images/choice_ui.png')


    def handle_collision(self, other):
        if self.num == 0:
            return False
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def select_collision(self):
        if self.selected:
            common.selecting = True
            print(1)
            if self.money[self.num] <= common.hero.money:
                print(2)
                common.hero.money -= self.money[self.num]
                apply_old_resources(self.num)
                self.buy = True
            common.selecting = False
            self.selected = False
        else:
            return

    def get_bb(self):
        if not self.num ==0:
            half_w = house_shop_select_data[1]['width']
            return self.x - half_w - select_offset, BOTTOM_OFFSET , self.x + half_w+select_offset, SCREEN_HEIGHT
        else:
            return 0,0,0,0

    def update(self):
        self.x -= common.background.display_speed * game_framework.frame_time
        self.select_collision()
        if self.x < - 55:
            self.exist = False
            game_world.remove_object(self)

    def draw(self):
        i = self.num
        w = self.w
        h = self.h
        if not self.buy:
            self.image.clip_draw(int(house_shop_select_data[i]["x"]),
                                 int(house_shop_select_data[i]['y']),
                                 int(house_shop_select_data[i]['width']),
                                 int(house_shop_select_data[i]['height']),
                                 self.x, self.y + self.h //2, w, h)
        else:
            self.buy_house_image.clip_draw(int(sell_house_data[i]["x"]),int(sell_house_data[i]["y"]),int(sell_house_data[i]["width"]),int(sell_house_data[i]["height"]),self.x, self.y + self.h //2, w, h)
        if not self.num == 0:
            self.choice_img.draw(self.x, self.y + self.h // 2 + 40 + h // 2, 150, 50)
            draw_rectangle(*self.get_bb())

class Propose:
    def __init__(self,num = 0):
        self.image = load_image('Images/propose_woman.png')
        if num == 0:
            self.w = propose_woman_data[num]['width'] * 3.2
            self.h = propose_woman_data[num]['height'] * 3.4
            self.y = common.hero.y + 15
        self.num = num
        self.x = 1310
        self.pos = common.background.map_total_w[10] ## 아무값이나 넣어놓기
        self.exist = False
        self.selected = False
        self.can_select = True

        self.success = 0 #-1실패 0초기 1성공

        self.choice_img = load_image('Images/choice_ui.png')

    def handle_collision(self, other):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def select_collision(self):
        if self.selected:
            common.selecting = True
            x = random.randrange(0, 100)
            if x <= common.propose_probality:
                self.success = 1
                common.skills[2].skill_earn = True
                common.hero.happy = min(100, common.hero.happy + 30)
                self.num = 2
            else:
                self.success = -1
                common.hero.happy = max(10,common.hero.happy - 20)
                self.num = 3
            common.skills[2].skill_earn = True
            common.selecting = False
            self.selected = False
            self.h += 7
            self.w += 15
            self.x -= 7
        else:
            return

    def get_bb(self):
        half_w = propose_woman_data[0]['width']
        return self.x - half_w - select_offset, BOTTOM_OFFSET , self.x + half_w+select_offset, SCREEN_HEIGHT

    def update(self):
        self.select_collision()
        self.x -= common.background.display_speed * game_framework.frame_time
        if self.x < - 55:
            self.exsit = False
            game_world.remove_object(self)

    def draw(self):
        i = self.num
        w = self.w
        h = self.h
        self.choice_img.draw(self.x, self.y + self.h //2 + 40+ h//2, 150, 50)

        self.image.clip_draw(int(propose_woman_data[i]["x"]),
                             int(propose_woman_data[i]['y']),
                             int(propose_woman_data[i]['width']),
                             int(propose_woman_data[i]['height']),
                             self.x, self.y + self.h //2, w, h)
        draw_rectangle(*self.get_bb())

class Friend:
    def __init__(self):
        self.image = load_image('Images/friend_idle.png')
        self.w = self.image.w * 1.9
        self.h = self.image.h * 1.9
        self.y = 100 + self.h //2
        self.x = 1310
        self.pos = common.background.map_total_w[3] - common.background.frame_w[3] * 3
        self.exist = False
        self.selected = False
        self.can_select = True
        self.success = 0 #-1실패 0초기 1성공

        self.choice_img = load_image('Images/choice_ui.png')

    def handle_collision(self, other):
        left_a, bottom_a, right_a, top_a = self.get_bb()
        left_b, bottom_b, right_b, top_b = other.get_bb()

        if left_a > right_b: return False
        if right_a < left_b: return False
        if top_a < bottom_b: return False
        if bottom_a > top_b: return False

        return True

    def select_collision(self):
        if self.selected:
            common.selecting = True
            x = random.randrange(0, 100)
            if x<= 80:
                self.success = 1
                common.skills[1].skill_earn = True
                common.hero.happy = min(100,common.hero.happy + 10)
            else:
                self.success = -1
                common.hero.happy -= 5
            self.h += 28
            self.w += 20
            self.y = 100 + self.h // 2
            common.selecting = False
            self.selected = False

    def get_bb(self):
        half_w = self.h //2
        return self.x - half_w - select_offset +5, self.y - self.h//2 , self.x + half_w+select_offset-5, self.y + self.h//2

    def update(self):
        self.x -= common.background.display_speed * game_framework.frame_time
        self.select_collision()
        if self.x < - 55:
            self.exsit = False
            game_world.remove_object(self)

    def draw(self):
        w = self.w
        h = self.h
        self.choice_img.draw(self.x, self.y + self.h //2 + 40+ h//2, 150, 50)

        if self.success == 1:
            self.image = load_image('Images/friend_success.png')
        elif self.success == -1:
            self.image = load_image('Images/friend_fail.png')

        self.image.draw(self.x, self.y, w, h)
        draw_rectangle(*self.get_bb())
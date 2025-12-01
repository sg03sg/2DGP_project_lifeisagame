from pico2d import *
import random
import game_world
import game_framework
from item import Item


class ItemSpawner:
    def __init__(self, itemlist, init_spawn_interval=1.5):
        self.itemlist = itemlist
        self.base_spawn_interval = [
            [timer for timer in per_age_timer]
            for per_age_timer in self.itemlist.y_timer_interval
        ]
        self.init_spawn_interval = init_spawn_interval

        # 나이/아이템 타입별 스폰 카운트
        # itemlist.max_item_count 와 동일한 모양으로 0으로 초기화
        self.item_spawn_count = [
            [0 for _ in per_age_limits]
            for per_age_limits in self.itemlist.max_item_count
        ]

        # 나이/아이템번호 타입별 확률 테이블
        self.item_probabilities = [
            [100],                 # age 0 : babymilk
            [100],                 # age 1 : smart
            [25, 25, 25, 25],      # age 2 : study / paint / soccer / music
        ]

        # 현재 필드에 존재하는 아이템들 저장용
        self.exist_items = []

        # 마지막으로 처리한 나이
        self.last_age = None

        # 현재 age에 대해 y축마다 하나씩 가지는 "다음 스폰 시간" 리스트
        self.y_spawn_times = []

    # 나이가 바뀌었을 때 호출:
    #- 이전 나이에서 만들어진 아이템 정리
    #- 현재 나이에 맞게 y축 타이머 재설정
    def reset_for_age(self, age):
        # 이전 나이의 아이템 정리
        for it in list(self.exist_items):
            if it.age != age:
                try:
                    game_world.remove_object(it)
                except ValueError:
                    pass
                try:
                    self.exist_items.remove(it)
                except ValueError:
                    pass

        self.last_age = age
        self.y_spawn_times = []

        # 해당 age에 대한 y 위치 정보가 없으면 끝
        if age >= len(self.itemlist.item_pos):
            return

        now = game_framework.game_time

        offset = min(self.base_spawn_interval[age])

        # 각 저장한 y 위치마다 하나씩 타이머 생성
        for i in range(len(self.itemlist.item_pos[age])):
            interval = self.base_spawn_interval[age][i] - offset
            self.y_spawn_times.append(now + interval)


    #아이템 결정 함수
    # - limit[age][item_idx] 보다 소환 카운트가 적은 것중에서 랜덤 선택
    # - 후보들에 대해서만 확률 재계산 후 랜덤 선택
    # - 더 이상 소환 가능 아이템이 없으면 None 반환
    def select_item(self, age):
        # age 범위를 벗어난 경우 예외 처리
        if age >= len(self.item_probabilities):
            return None

        probs_for_age = self.item_probabilities[age]
        limits = self.itemlist.max_item_count[age]
        counts = self.item_spawn_count[age]

        # 아직 limit를 넘지 않은 아이템들 모음
        no_limit_items = [
            i for i in range(len(probs_for_age))
            if counts[i] < limits[i]
        ]

        # 모든 아이템이 limit에 도달했을때 예외처리
        if not no_limit_items:
            return None

        # 후보 아이템들의 확률만 모아서 다시 가중치 적용
        weights = [probs_for_age[i] for i in no_limit_items]
        total = sum(weights)
        if total == 0:
            return None
        r = random.randint(0, total)

        acc = 0
        for idx, w in zip(no_limit_items, weights):
            acc += w
            if r <= acc:
                return idx

        # y축 타이머들 관리
        # - 기본 간격은 base_spawn_interval
        # - 40% 확률로 타이머 간격 줄이기
    def timer_for_y(self, index, now,age):
        interval = self.base_spawn_interval[age][index]
        if random.random() < 0.25:
            # 너무 짧아지지 않도록 최소값 설정
            interval = 1.0
        self.y_spawn_times[index] = now + interval


    def update(self, hero):
        age = hero.age

        # 나이가 바뀌었으면 그에 맞게 정리+타이머 초기화
        if age != self.last_age:
            self.reset_for_age(age)

        # 해당 age에 대한 y 위치 정보가 없으면 할 일 없음
        if age >= len(self.itemlist.item_pos):
            return

        now = game_framework.game_time

        # 각 y축별 타이머 체크
        for i, y in enumerate(self.itemlist.item_pos[age]):
            # 방어 코드: y_spawn_times 길이가 맞지 않을 경우
            if i >= len(self.y_spawn_times):
                continue

            # 아직 이 y축의 타이머가 안 됐으면 패스
            if now < self.y_spawn_times[i]:
                continue

            # 이 나이에서 어떤 아이템을 뽑을지 확률 기반으로 결정
            item_index = self.select_item(age)

            # 소환 가능한 아이템이 더 이상 없으면
            # 이 y축은 앞으로도 소환하지 않도록 타이머를 무한대로
            if item_index is None:
                self.y_spawn_times[i] = float('inf')
                continue

            # 아이템 생성 및 월드에 추가
            item = Item(None, y, age, item_index)
            game_world.add_object(item, 1)
            game_world.add_collision_pair('hero:item', None, item)
            self.exist_items.append(item)

            # 지금까지 소환된 해당 아이템의 갯수 +1
            self.item_spawn_count[age][item_index] += 1

            # 이 y축 타이머 리셋 (40% 확률로 간격 -0.5초)
            self.timer_for_y(i, now,age)

    # 스테이지 전환 등에서 스포너 초기화할 때 사용.
    # - 필드에 남아있는 아이템 제거
    # - 타이머/나이 정보 초기화
    def clear(self):
        for it in list(self.exist_items):
            try:
                game_world.remove_object(it)
            except ValueError:
                pass
        self.exist_items.clear()

        self.y_spawn_times = []
        self.last_age = None

        # 게임 전체를 리셋할  타이머 아예 초기화
        # self.item_spawn_count = [
        #     [0 for _ in per_age_limits]
        #     for per_age_limits in self.itemlist.max_item_count
        # ]
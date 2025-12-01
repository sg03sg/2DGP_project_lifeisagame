from pico2d import *
import random
import game_world
import game_framework
from item import Item


class ItemSpawner:
    def __init__(self, itemlist, base_spawn_interval=1.5):
        self.itemlist = itemlist
        self.base_spawn_interval = float(base_spawn_interval)

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

        # 각 저장한 y 위치마다 하나씩 타이머 생성
        for _ in self.itemlist.item_pos[age]:
            self.y_spawn_times.append(now + self.base_spawn_interval)


    #아이템 결정 함수
    # - limit[age][item_idx] 보다 소환 카운트가 적은 것중에서 랜덤 선택
    # - 후보들에 대해서만 확률 재계산 후 랜덤 선택
    # - 더 이상 소환 가능 아이템이 없으면 None 반환
    def select_item(self, age):
        pass



        # y축 타이머들 관리
        # - 기본 간격은 base_spawn_interval
        # - 40% 확률로 타이머 간격 줄이기
    def timer_for_y(self, index, now):
        pass


    def update(self, hero):
        pass

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
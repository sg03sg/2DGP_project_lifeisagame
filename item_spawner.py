# ...new file...
from pico2d import *
import random
import game_world
import game_framework
from item import Item

class ItemSpawner:
    def __init__(self, itemlist, spawn_interval=1.5):
        # itemlist: Itemlist 인스턴스 (item_pos 포함)
        self.itemlist = itemlist
        self.spawn_interval = float(spawn_interval)
        self.last_spawn = game_framework.game_time
        self.exist_items = []
        self.last_age = 0

    def update(self, hero):
        # 나이 변경에 따라 이전 나이용 아이템 삭제
        if hero.age != self.last_age:
            removes = [it for it in self.exist_items if it.age != hero.age]
            for it in removes:
                try:
                    game_world.remove_object(it)
                except ValueError:
                    pass
                if it in self.exist_items:
                    self.exist_items.remove(it)
            self.last_age = hero.age

        # 스폰 타이밍 체크
        now = game_framework.game_time
        if now - self.last_spawn >= self.spawn_interval:
            # 해당 나이에 아이템 위치 정보가 없으면 패스
            if len(self.itemlist.item_pos) <= hero.age:
                self.last_spawn = now
                return

            item_y = random.choice(self.itemlist.item_pos[hero.age])
            item = Item(None, item_y, hero.age)
            game_world.add_object(item, 1)
            game_world.add_collision_pair('hero:item', None, item)
            self.exist_items.append(item)
            self.last_spawn = now

    def clear(self):
        for it in list(self.exist_items):
            try:
                game_world.remove_object(it)
            except ValueError:
                pass
            try:
                self.exist_items.remove(it)
            except ValueError:
                pass


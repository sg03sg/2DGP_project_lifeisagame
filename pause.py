import common

class Pause_test:
    def __init__(self, pause_def,age = 0):
        self.pause_def = pause_def
        self.break_map = False
        self.select_job = False
        self.last_age = age

    def update(self,age):
        if self.last_age == 2 and age == 3:
            self.select_job = True

        print(f'{common.background.map_idx}')
        if common.background.map_idx == 2:
            self.break_map = True
        else:
            self.break_map = False

        # print(f'{self.break_map}')
        if self.break_map:
            self.pause_def.pause_item_and_clear()
        else:
            self.pause_def.resume_item()

        print('pause_item after:', common.item_spawner.stop, id(common.item_spawner))

        # if self.select_job:
        #     self.pause_def.pause_game_switch()
        # else:
        #     self.pause_def.resume_game_switch()

class Pause:
    def pause_item_and_clear(self):
        if common.item_spawner.exist_items:
            common.item_spawner.clear()
        common.item_spawner.stop = True

    def pause_item(self):
        if common.item_spawner.exist_items:
            for item in common.item_spawner.exist_items:
                item.stop = True
        common.item_spawner.stop = True

    def resume_item(self):
        if common.item_spawner.exist_items:
            for item in common.item_spawner.exist_items:
                item.stop = False
        common.item_spawner.stop = False

    def pause_game_switch(self):
        common.background.stop = True
        common.hero.stop = True
        self.pause_item()

    def resume_game_switch(self):
        common.background.stop = False
        common.hero.stop = False
        self.resume_item()

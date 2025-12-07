from pico2d import *
import game_world
import game_framework
import background
import play_mode
import common
import savelist

stu_it_num = [5,6,7,8]
with open('Json/ui_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('Json/adult_item_data.json', 'r', encoding='utf-8') as f:
    adult_item_data = json.load(f)
##아이템 번호 뽑는 작업
stu_item_data = [data['sprites'][i] for i in stu_it_num]

class Item:
    image = None

    def __init__(self, filename = None,y = 150,age=0, num=0):
        if filename == None:
            filename = ['Images/ITEMIMAGE_babymilk.png','Images/item_smart.png','Images/ui.png','Images/adult_item.png']

        self.age = age
        self.num = num
        name = [['babymilk'],['smart'],['study','paint','music','soccer'],['coin','cigarette','dumbel','hambuger','pizza','ramen'], ['coin','cigarette','dumbel','hambuger','pizza','ramen']]
        self.name = name[age][num]
        self.images = [load_image(f) for f in filename]
        self.x = 1300
        self.y = y
        self.speed = background.RUN_SPEED_PPS + 500  # 아이템의 속도 (배경보다 빠르게)
        self.xv = -self.speed  # x 축 속도
        self.size = [40,40,60,50,50]

        self.stop = False

    def get_bb(self):
        s = self.size[self.age] // 2
        return self.x - s, self.y - s, self.x + s, self.y + s

    def draw(self):
        if self.age == 2:
            self.images[self.age].clip_draw( int( stu_item_data[self.num]["x"]),
                                             int( stu_item_data[self.num]["y"]),
                                             int( stu_item_data[self.num]["width"]),
                                             int( stu_item_data[self.num]["height"]),
                                             self.x, self.y,self.size[self.age],self.size[self.age])
        elif self.age == 3 or self.age ==4:
            self.images[3].clip_draw( int( adult_item_data["sprites"][self.num]["x"]),
                                             int( adult_item_data["sprites"][self.num]["y"]),
                                             int( adult_item_data["sprites"][self.num]["width"]),
                                             int( adult_item_data["sprites"][self.num]["height"]),
                                             self.x, self.y,self.size[3],self.size[3])
        else:
            self.images[self.age].draw(self.x, self.y,40,40)
        draw_rectangle(*self.get_bb())

    def handle_collision(self,group, other):
        if group == 'hero:item':
            game_world.remove_object(self)
            common.item_spawner.exist_items.remove(self)
            if self.age == 2:
                common.job_stat.handle_collision(self)
                return
            self. item_updown_stats()


    def update(self):
        if self.stop:
            return
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time
        if self.x <= 0:
            game_world.remove_object(self)
            common.item_spawner.exist_items.remove(self)

    def item_updown_stats(self):
        item_name = self.name
        effects = savelist.item_stats.get(item_name, {})

        for stat, amount in effects.items():
            new_value = getattr(common.hero, stat) + amount

            # 0~100 범위 제한 스탯들 제한
            if stat in ('happy', 'health', 'smarter'):
                new_value = clamp(0, new_value, 100)

            setattr(common.hero, stat, new_value)


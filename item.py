from pico2d import *
import game_world
import game_framework
import background
import play_mode
import common

stu_it_num = [5,6,7,8]
with open('Json/ui_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
##아이템 번호 뽑는 작업
stu_item_data = [data['sprites'][i] for i in stu_it_num]

class Item:
    image = None

    def __init__(self, filename = None,y = 150,age=0, num=0):
        if filename == None:
            filename = ['Images/ITEMIMAGE_babymilk.png','Images/item_smart.png','Images/ui.png']

        self.age = age
        self.num = num
        name = [['babymilk'],['smart'],['study','paint','music','soccer']]
        self.name = name[age][num]
        self.images = [load_image(f) for f in filename]
        self.x = 1300
        self.y = y
        self.speed = background.RUN_SPEED_PPS + 400  # 아이템의 속도 (배경보다 빠르게)
        self.xv = -self.speed  # x 축 속도
        self.size = [40,40,60]

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
            if self.name == 'smart':
                common.hero.smarter += 1
                if common.hero.smarter >100:
                    common.hero.smarter = 100


    def update(self):
        if self.stop:
            return
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time
        if self.x <= 0:
            game_world.remove_object(self)
            common.item_spawner.exist_items.remove(self)



inf = float('inf')
class Itemlist:
    def __init__(self):
        self.item_pos = [[150 ,350], [570],[550,450,350,250,150]]
        self.max_item_count = [[inf], [inf] , [9,9,9,9] ]
        self.y_timer_interval = [[1.5,3.0], [1.2], [2.0,3.0,3.5,4.0,5.0]]

class Uilist:
    def __init__(self):
        self.skillname = ['hobby', 'friend', 'family']

        self.age1uiname = ['smart', 'baby', 'painting']
        self.age1ui_max_count = [9, 3, 3]
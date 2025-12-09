inf = float('inf')
item_pos = [[150 ,350], [570],[600,500,400,300,150], [600,500,300,150], [600,500,300,150]]
max_item_count = [[inf], [inf] , [11,11,11,11], [inf,inf,inf,inf,inf,inf], [inf,inf,inf,inf,inf,inf]]
y_timer_interval = [[2.0,3.5], [1.5], [4.0,4.5,5.5,6.5,7.0], [3.0,3.5,4.0,4.5], [3.0,3.5,4.0,4.5]]
skillname = ['hobby', 'friend', 'family']

## -------------------------------------------
age1uiname = ['smart', 'baby', 'painting']
age2uiname = ['study', 'paint', 'music', 'soccer']
age3and4uiname = ['cigarette']
age1ui_max_count = [9, 3, 3]
age2ui_max_count = [9, 9, 9, 9]
age3and4ui_max_count = [7]


##-------------------------------------------
job = {0: 'no_job', 1:'study', 2 : 'paint', 3 : 'music', 4 : 'soccer'}

# [['babymilk'], ['smart'], ['study', 'paint', 'music', 'soccer'],
#         ['coin', 'cigarette', 'dumbel', 'hambuger', 'pizza', 'ramen'],
#         ['coin', 'cigarette', 'dumbel', 'hambuger', 'pizza', 'ramen']]
item_stats = {
    'babymilk':   {'happy': +5},
    'smart':      {'happy': +3, 'smarter': +1},
    'study': {'happy': -4},
    'paint': {'happy': -2},
    'music': {'happy': -2},
    'soccer': {'happy': -2},
    'coin':       {'happy': -5, 'money': +40},
    'cigarette':  {'happy': +5, 'hp': -5,'smoking': +1},
    'dumbel':     {'happy': +2, 'hp': +1},
    'hambuger':   {'happy': +2, 'hp': -1},
    'pizza':      {'happy': +2, 'hp': -1},
    'ramen':      {'happy': +2, 'hp': -1},
}

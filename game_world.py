world = [[], []]

def add_object(o,depth=0):
    world[depth].append(o)

def add_objects(ol, depth = 0):
    world[depth] += ol

def update():
    for layer in world:
        for o in layer:
            o.update()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')

def draw():
    for layer in world:
        for o in layer:
            o.draw()

def clear():
    global world

    for layer in world:
        layer.clear()
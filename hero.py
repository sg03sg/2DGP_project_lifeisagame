from pico2d import load_image
import state_machine
from state_machine import StateMachine


class Run:
    def __init__(self,hero):
        self.hero = hero

    def enter(self):
        pass

    def exit(self):
        pass

    def do(self):
        self.hero.frame = (self.hero.frame+1)%10
        if self.hero.frame %10 ==0:
            self.hero.y_frame = (self.hero.y_frame +1)%3
    def draw(self):
        self.hero.image.clip_composite_draw(self.hero.frame * 153, 323 - self.hero.y_frame * 113, 120, 90, 0, 'h', self.hero.x, self.hero.y, 100,
                                       100)


class Idle:
    def __init__(self, hero):
        self.hero = hero

    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Jump:
    def __init__(self, hero):
        self.hero = hero

    def enter(self):
        pass
    def exit(self):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Hero:
    def __init__(self):
        self.x, self.y = 640, 150
        self.frame = -1
        self.y_frame =-1
        self.image = load_image('nobaby.png')

        self.run = Run(self)
        self.idle = Idle(self)
        self.jump = Jump(self)
        self.state_machine = StateMachine(
              self.run)


    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        pass
        # self.state_machine.handle_state_event(("INPUT", event))

from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
from state_machine import StateMachine

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def jump_end(e):
    return e[0] == 'jump_end'

def No(e):
    return False

def hero_jump(hero, dt):
    hero.jump_vy += hero.gravity * dt
    hero.y += hero.jump_vy * dt
    # 착지 검사
    if hero.y <= 150:
        hero.y = 150
        hero.jump_vy = 0.0
        hero.state_machine.handle_state_event(("jump_end", None))


class Run:
    def __init__(self,hero):
        self.hero = hero

    def enter(self,e):
        pass

    def exit(self,e):
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

    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass

class Jump:
    def __init__(self, hero):
        self.hero = hero

    def enter(self,e):
        # 점프 시작 시 초기 속도 설정
        self.hero.jump_vy = self.hero.jump_initial_v

    def exit(self,e):
        pass

    def do(self):
        # dt는 lifeisagame.py의 delay 값과 맞춰 사용
        dt = 0.02
        hero_jump(self.hero, dt)

    def draw(self):
        self.hero.image.clip_composite_draw(self.hero.frame * 153, 323 - self.hero.y_frame * 113, 120, 90, 0, 'h',
                                            self.hero.x, self.hero.y, 100,
                                            100)

class Hero:
    def __init__(self):
        self.x, self.y = 640, 150
        self.frame = -1
        self.y_frame =-1
        self.image = load_image('nobaby.png')

        # 점프 관련 기본값 : v0^2 / (2 * |g|) <-이거 계산하면 최고 높이
        self.jump_initial_v = 1300.0    # 초기 상승 속도(px/s)
        self.gravity = -2100.0         # 중력(px/s^2)
        self.jump_vy = 0.0

        self.run = Run(self)
        self.idle = Idle(self)
        self.jump = Jump(self)
        self.state_machine = StateMachine(
              self.run,
        {
                self.run: {space_down: self.jump},
                self.jump: {jump_end: self.run},
                self.idle: {No: self.idle},
             }
        )


    def update(self):
        self.state_machine.update()
        pass

    def draw(self):
        self.state_machine.draw()
        pass

    def handle_event(self, event):
        self.state_machine.handle_state_event(("INPUT", event))

from pico2d import *
import play_mode as start_mode
import title_mode
import game_framework

open_canvas(1280,720)
# game loop
game_framework.run(title_mode)
close_canvas()

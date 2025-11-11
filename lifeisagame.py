from pico2d import *
import play_mode

open_canvas(1280,720)
play_mode.init()
# game loop
while play_mode.running:
    play_mode.handle_events()
    play_mode.update_world()
    play_mode.draw()
    delay(0.02)
play_mode.finish()
close_canvas()

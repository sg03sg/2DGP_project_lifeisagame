from pico2d import *


class Background:
    def __init__(self):
        # 이미지가 resource 폴더에 있으므로 경로를 수정
        self.image = load_image('spr_Babyroom_1.png')

    def draw(self):
        # 캔버스 크기에 맞게 중앙에 스케일하여 그리기
        w = get_canvas_width()
        h = get_canvas_height()
        self.image.draw(w // 2, h // 2, w, h)

    def update(self):
        pass

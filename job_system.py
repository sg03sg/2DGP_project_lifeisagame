from pico2d import *

import common


## hero에서 해당 클래스 선언하고 age2아이템과 충돌했을때 해당 스텟을 관리해주는 작업을 하는 함수 1
## age2 아이템 최종 스텟을 가지고 age3으로 넘어갈때 그에 맞는 직업을 반환하는 함수 (인덱스를 반환)
class Job_stat:
    def __init__(self):
        self.job_soccer = 0
        self.job_music = 0
        self.job_paint = 0
        self.job_study = 0

    ##함수 1
    def handle_collision(self, other):
            if other.name == 'study':
                self.job_study += 1
            elif other.name == 'paint':
                self.job_paint += 1
            elif other.name == 'music':
                self.job_music += 1
            elif other.name == 'soccer':
                self.job_soccer += 1

    ##함수 2
    def get_job(self):
        pass

## 선택 가능 직업변수
## 함수1:직업 관련 아이템의 획득 갯수를 가지고 max_item보다 크거나 같다면 선택할 수 있는 직업을 가지게 해줌
## 함수 2: 선택 가능 직업을 바탕으로 최종 직업 선택을 해주는 함수 age3로 넘어갈때 호출
class Job_select:
    def __init__(self):
        self.job_item_stat = common.job_stat  # 직업 관련 아이템 획득 통계
        self.select = False
        self.index = 0 # 현재 직업 인덱스
        self.wait_time = get_time()

    def compare_item_count(self, max_item_counts):
        self.selectable_jobs = []  # 선택 가능한 직업들
        pass

    def get_job(self,job):
        self.now_job = job
        if self.select:
            common.hero.job
        pass

    def update(self):
        self.compare_item_count(self.job_item_stat.count)
        max = len(self.selectable_jobs)
        time = get_time()
        if time - self.wait_time > 1:
            self.index = (self.index + 1) % max
            wait_time = time
        now_job = self.selectable_jobs[self.index]
        self.get_job(now_job)
        pass

    def draw(self):
        pass





from pico2d import *

import common

with open('Json/select_job_data.json', 'r', encoding='utf-8') as f:
    sel_job_data = json.load(f)

## hero에서 해당 클래스 선언하고 age2아이템과 충돌했을때 해당 스텟을 관리해주는 작업을 하는 함수 1
class Job_stat:
    def __init__(self):
        self.stats = [0, 0, 0, 0]  # study, paint, music, soccer

    ##함수 1
    def handle_collision(self, other):
            if other.name == 'study':
                self.stats[0] += 1
            elif other.name == 'paint':
                self.stats[1] += 1
            elif other.name == 'music':
                self.stats[2] += 1
            elif other.name == 'soccer':
                self.stats[3] += 1

## 선택 가능 직업변수
## 함수1:직업 관련 아이템의 획득 갯수를 가지고 max_item보다 크거나 같다면 선택할 수 있는 직업을 가지게 해줌
## 함수 2: 선택 가능 직업을 바탕으로 최종 직업 선택을 해주는 함수 age3로 넘어갈때 호출
class Job_select:
    def __init__(self):
        self.image = load_image('Images/select_job.png')
        age = common.hero.age
        self.x, self.y = common.hero.x + common.hero.side_size[age], common.hero.y + common.hero.tall[age]
        self.job_item_stat = common.job_stat  # 직업 관련 아이템 획득 통계
        self.select = False
        self.index = 0 # 현재 직업 인덱스
        self.wait_time = get_time()
        self.selectable_jobs = []  # 선택 가능한 직업들


    def compare_item_count(self, max_item_counts):
        for item_idx,v in enumerate(max_item_counts):
            if v <= self.job_item_stat.stats[item_idx]:
                self.selectable_jobs.append(item_idx)
        pass

    def get_job(self):
        if self.select:
            common.hero.job = self.now_job
        pass

    def update(self):
        self.compare_item_count(self.job_item_stat.count)
        max = len(self.selectable_jobs)
        time = get_time()
        if time - self.wait_time > 1:
            self.index = (self.index + 1) % max
            wait_time = time
        self.now_job = self.selectable_jobs[self.index]
        self.get_job()
        pass

    def draw(self):
        sel_job = sel_job_data['sprites'][self.now_job]
        self.image.clip_draw(int(sel_job["x"]),int(sel_job['y']),int(sel_job["width"]),int(sel_job["height"]),self.x,self.y,100,90)

    def select_collision(self):
        self.select = True




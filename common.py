from effect import Effect
from job_system import Job_stat
from pause import Pause

background = None
hero = None
item_spawner = None
pause_test = None

job_select = None
job_stat = Job_stat()
pause_def = Pause()

select_system = None
selecting = False

skills = None
skill_system = None

effect = Effect()

speed = 5.0
hobby_num = 0

propose_probality = 50  # 프러포즈 확률 %
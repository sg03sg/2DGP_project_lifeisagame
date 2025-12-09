from effect import Effect
from ending_system import Ending_system
from job_system import Job_stat
from pause import Pause

background = None
hero = None
item_spawner = None
pause_test = None

job_select = None
job_stat = None
pause_def = Pause()

select_system = None
selecting = False

skills = None
skill_system = None

effect = Effect()

speed = 5.0
hobby_num = 0

propose_probality = 0  # 프러포즈 확률 %

ending_system = None

def initialize():
    global background
    global hero
    global item_spawner
    global pause_test
    global job_select
    global select_system
    global skills
    global skill_system
    background = None
    hero = None
    item_spawner = None
    pause_test = None

    job_select = None
    job_stat = Job_stat()

    select_system = None
    selecting = False

    skills = None
    skill_system = None

    effect = Effect()

    speed = 5.0
    hobby_num = 0

    propose_probality = 50  # 프러포즈 확률 %
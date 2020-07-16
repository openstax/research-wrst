# The Experiment class is the basic setup for all experiments (Prolific, Psych pool, etc)

# reading_links contain the readings that each cohort does, it must have the same length as cohort_names
# reading_time is the time required to complete a reading in minutes??
# task_time is time spent on the actual relationships selection task

# redirect_link is the redirect_link supplied by Prolific for your experiment
# All of the times are in seconds so handle accordingly

from wrst.logic.task_block import TaskBlock, ReadingTask, QualtricsTask, TaskQueue, WRSTTask, DistractorTask

instruction_task = TaskBlock(task_name='instruction',
                             task_starting_route='instruction_routes.display_task_instructions')
reading_task = ReadingTask(task_name='reading',
                           task_starting_route='reading_routes.display_reading_instructions',
                           reading_link="https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells",
                           reading_time=10
                           )
training_task = TaskBlock(task_name='training',
                          task_starting_route='training_routes.training_1')

wrst_task = WRSTTask(task_name='wrst',
                     task_starting_route='wrst_routes.get_new_task',
                     task_time=5)


wrst_task2 = WRSTTask(task_name='wrst2',
                     task_starting_route='wrst_routes.get_new_task',
                     task_time=5)

distractor_task1 = DistractorTask(task_name='2048',
                                 task_starting_route='distractor_routes.distractor_task',
                                 task_time=10)

distractor_task2 = DistractorTask(task_name='2048_2',
                                 task_starting_route='distractor_routes.distractor_task',
                                 task_time=10)

qualtrics_task = QualtricsTask(task_name='qualtrics_2_question',
                               task_starting_route='https://riceuniversity.co1.qualtrics.com/jfe/form/SV_81ynJttKNymIieV')

end_task = TaskBlock(task_name='final',
                     task_starting_route='instruction_routes.psych_final')

task_queue = TaskQueue(task_block_list=[instruction_task,
                                        reading_task,
                                        distractor_task1,
                                        wrst_task,
                                        wrst_task2,
                                        qualtrics_task,
                                        distractor_task2,
                                        end_task]
                       )




class Experiment():
    def __init__(self):
        self.reading_links = ["https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells",
                              "https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells"]
                              #"https://openstax.org/books/biology-2e/pages/4-2-the-cell-cycle"]
                              #"https://openstax.org/books/biology-2e/pages/10-4-cancer-and-the-cell-cycle"]
                              #"https://openstax.org/books/biology-2e/pages/10-2-the-cell-cycle"]

        self.cohort_names = ['a', 'b'] ###UPDATE BEFORE PUSHING
        # self.cohort_names = ['a'] # ['a', 'b']
        self.num_cohorts = len(self.cohort_names)

class ProlificExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 5 # Change reading time to 5
        self.task_time = 5 # Change task time to 25
        self.redirect_link = "https://app.prolific.co/submissions/complete?cc=15797BE5" 

class PsychExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 1*60 #set reading time, currently in seconds
        self.task_time = 30*60

class TestExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 5
        self.task_time = 30*60

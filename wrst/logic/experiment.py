# The Experiment class is the basic setup for all experiments (Prolific, Psych pool, etc)

# reading_links contain the readings that each cohort does, it must have the same length as cohort_names
# reading_time is the time required to complete a reading in minutes??
# task_time is time spent on the actual relationships selection task

# redirect_link is the redirect_link supplied by Prolific for your experiment
# All of the times are in seconds so handle accordingly

from wrst.logic.task_block import TaskBlock, ReadingTask, ReReadingTask, QualtricsTask, TaskQueue, WRSTTask, DistractorTask

instruction_task = TaskBlock(task_name='instruction',
                             task_starting_route='instruction_routes.display_task_instructions')

instruction_task_peda = TaskBlock(task_name='instruction_pedagogical',
                             task_starting_route='instruction_routes.display_pedagogical_evaluation_instructions')

instruction_task_encoding = TaskBlock(task_name='instruction_encoding',
                             task_starting_route='instruction_routes.display_encoding_instructions')

instruction_task_distractor = TaskBlock(task_name='instruction_distractor',
                             task_starting_route='instruction_routes.display_distractor_instructions')

instruction_quiz = TaskBlock(task_name='instruction_quiz',
                             task_starting_route='instruction_routes.display_quiz_instructions')

instruction_retrieval = TaskBlock(task_name='instruction_retrieval',
                             task_starting_route='instruction_routes.display_retrieval_instructions')


reading_task = ReadingTask(task_name='reading',
                           task_starting_route='reading_routes.display_reading_instructions',
                           reading_link="https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells",
                           reading_time=15*60
                           )

reading_task_psych = ReadingTask(task_name='reading',
                           task_starting_route='reading_routes.display_reading_instructions',
                           reading_link="https://openstax.org/books/psychology-2e/pages/14-1-what-is-stress",
                           reading_time=15*60
                           )


rereading_task = ReReadingTask(task_name='rereading',
                           task_starting_route='reading_routes.display_rereading_instructions',
                           reading_link="https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells",
                           reading_time=15*60
                           )


training_task_bio = TaskBlock(task_name='training',
                          task_starting_route='training_routes.training_1_pedagogical_eval')


training_task_psych = TaskBlock(task_name='training',
                                task_starting_route='training_routes_psych.training_1_psych')

training_task_psych_part2 = TaskBlock(task_name='training2',
                                task_starting_route='training_routes_psych.training_19_psych')


training_task_reading = TaskBlock(task_name='reading_training',
                                task_starting_route='reading_training_routes.reading_training_1')

training_task_retrieval = TaskBlock(task_name='retrieval_training',
                                task_starting_route='retrieval_training_routes.retrieval_training_1')

wrst_task = WRSTTask(task_name='wrst',
                     task_starting_route='wrst_routes.get_new_task',
                     task_time=15*60
                     )


distractor_task1 = DistractorTask(task_name='2048',
                                 task_starting_route='distractor_routes.distractor_task',
                                 task_time=10*60
                                )

distractor_task2 = DistractorTask(task_name='2048_2',
                                 task_starting_route='distractor_routes.distractor_task',
                                 task_time=10)

qualtrics_retrieval_task = QualtricsTask(task_name='external_retrieval_practice',
                               task_starting_route='https://riceuniversity.co1.qualtrics.com/jfe/form/SV_cv9Z7Oyicouh66y')


qualtrics_task = QualtricsTask(task_name='bio_4_2_quiz_a',
                               task_starting_route='https://riceuniversity.co1.qualtrics.com/jfe/form/SV_3Dhy4ALx66ao33w')
#bio_42_first_link = 'https://riceuniversity.co1.qualtrics.com/jfe/form/SV_3Dhy4ALx66ao33w'
#bio_42_second_link = 'https://riceuniversity.co1.qualtrics.com/jfe/form/SV_elLIUNC2vYy9tae'
#bio_42_reading_first_link = 'https://riceuniversity.co1.qualtrics.com/jfe/form/SV_eX4nqMQaCGEWQ9o'


psych_quiz_a = QualtricsTask(task_name='psych_14_1_quiz_a',
                             task_starting_route='https://riceuniversity.co1.qualtrics.com/jfe/form/SV_3kMU29Dny5g0OR8')

psych_quiz_b = QualtricsTask(task_name='psych_14_1_quiz_b',
                             task_starting_route='https://riceuniversity.co1.qualtrics.com/jfe/form/SV_bfttpWdaxuwJOtw')


end_task = TaskBlock(task_name='final',
                     task_starting_route='instruction_routes.prolific_final')

#task_queue_bio = TaskQueue(task_block_list=[instruction_task_peda,
#                                        #training_task_reading,
#                                        training_task_retrieval,
#                                        reading_task,
#                                        instruction_retrieval,
#                                        qualtrics_retrieval_task,
#                                        instruction_task_distractor,
#                                        distractor_task1,
#                                        instruction_quiz,
#                                        qualtrics_task,
#                                        end_task]
#                       )

# Psych queue
task_queue = TaskQueue(task_block_list=[instruction_task_peda,
                                        #training_task_reading,
                                        training_task_psych,
                                        reading_task_psych,
                                        training_task_psych_part2,
                                        wrst_task,
                                        instruction_task_distractor,
                                        distractor_task1,
                                        instruction_quiz,
                                        psych_quiz_a,
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

# The Experiment class is the basic setup for all experiments (Prolific, Psych pool, etc)

# reading_links contain the readings that each cohort does, it must have the same length as cohort_names
# reading_time is the time required to complete a reading in minutes??
# task_time is time spent on the actual relationships selection task

# redirect_link is the redirect_link supplied by Prolific for your experiment
# All of the times are in seconds so handle accordingly

class Experiment():
    def __init__(self):
        self.reading_links = ["https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells",
                              "https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells"]#,
                              #"https://openstax.org/books/biology-2e/pages/10-4-cancer-and-the-cell-cycle"]

        self.cohort_names = ['a', 'b'] ###UPDATE BEFORE PUSHING
        # self.cohort_names = ['a'] # ['a', 'b']
        self.num_cohorts = len(self.cohort_names)

class ProlificExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 1*60 # Change reading time to 5
        self.task_time = 3*60 # Change task time to 25
        self.redirect_link = "https://app.prolific.co/submissions/complete?cc=15797BE5" 

class PsychExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 1*60 #set reading time, currently in seconds
        self.task_time = 3*60

class TestExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 5
        self.task_time = 30

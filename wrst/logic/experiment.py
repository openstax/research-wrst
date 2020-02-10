# The Experiment class is the basic setup for all experiments (Prolific, Psych pool, etc)
# reading_links contain the readings that each cohort does, it must have the same length as cohort_names
# reading_time is the time required to complete a reading
# task_time is time spent on the actual relationships selection task
class Experiment():
    def __init__(self):
        self.reading_links = ["https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells",
                              "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"]
        self.cohort_names = ['a', 'b']
        self.num_cohorts = len(self.cohort_names)

class ProlificExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 10*60
        self.task_time = 20*60
        self.redirect_link = 'https://app.prolific.co/submissions/complete?cc=1778FC3A'

class PsychExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 10*60
        self.task_time = 20*60

class TestExperiment(Experiment):
    def __init__(self):
        Experiment.__init__(self)
        self.reading_time = 5
        self.task_time = 5*60

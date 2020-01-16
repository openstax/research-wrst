class Reading(self, content_filter, time_allotted, redirect_link):
    self.content_filter = content_filter
    self.time_allotted = time_allotted
    self.redirect_link = redirect_link

class WRST(self, content_filter, time_alloted, redirect_link):
    self.content_filter = content_filter
    self.time_allotted = time_allotted
    self.redirect_link = redirect_link

class InstructionPage(self, redirect_link):
    self.redirect_link = redirect_link
    self.content_filter = None
    self.time_allotted = None


# The Experiment class is the basic setup
# task_list is a dictionary of lists, one per cohort, with each list consisting of some set of task classes
# The task classes will be carried out sequentially
# The key for each dictionary is the cohort name
class Experiment():
    def __init__(self, experiment_name, task_dictionary):
        self.experiment_name = experiment_name
        self.num_cohorts = len(task_list.keys())
        self.task_dictionary = task_dictionary


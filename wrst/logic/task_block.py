# Basic block for tasks (qualtrics survey, WRST matching, readings, etc)
# Each block contains, at a minimum, a unique task name (key), and a start route

from flask import redirect, url_for, request, session

class TaskBlock():
    def __init__(self, task_name, task_starting_route, variable_dictionary=None):
        self.task_name = task_name
        self.task_starting_route = task_starting_route
        self.variable_dictionary = variable_dictionary

    def get_starting_route(self):
        return url_for(self.task_starting_route)

class QualtricsTask(TaskBlock):
    def __init__(self, task_name, task_starting_route, variable_dictionary=None):
        super().__init__(task_name, task_starting_route, variable_dictionary)

    def get_starting_route(self):
        url = self.task_starting_route
        url += "?PROLIFIC_PID="
        url += session['user_id']
        return url

class ProlificReroute(TaskBlock):
    def __init__(self, task_name, task_starting_route, variable_dictionary=None):
        super().__init__(task_name, task_starting_route, variable_dictionary)

    def get_starting_route(self):
        url = self.task_starting_route
        url += "?PROLIFIC_PID="
        url += session['user_id']
        return url


class ReadingTask(TaskBlock):
    def __init__(self, task_name, task_starting_route, reading_link, reading_time=600, variable_dictionary=None):
        super().__init__(task_name, task_starting_route, variable_dictionary)
        self.reading_time = reading_time
        self.reading_link = reading_link

    def get_starting_route(self):
        session['required_reading_time'] = self.reading_time
        session['reading_link'] = self.reading_link
        return url_for(self.task_starting_route)

class WRSTTask(TaskBlock):
    def __init__(self, task_name, task_starting_route, task_time, variable_dictionary=None):
        super().__init__(task_name, task_starting_route, variable_dictionary)
        self.task_time = task_time

    def get_starting_route(self):
        session['required_time_on_task'] = self.task_time
        return url_for(self.task_starting_route)

class DistractorTask(TaskBlock):
    def __init__(self, task_name, task_starting_route, task_time, variable_dictionary=None):
        super().__init__(task_name, task_starting_route, variable_dictionary)
        self.task_time = task_time

    def get_starting_route(self):
        session['distractor_timeout'] = self.task_time
        return url_for(self.task_starting_route)

# The TaskQueue is simply a list of TaskBlocks . . . they will be executed sequentially
class TaskQueue():
    def __init__(self, task_block_list):
        self.task_block_list = task_block_list
        self.task_list_names = [t.task_name for t in self.task_block_list]
        print("Init")
        print(self.task_list_names)
        self.current_task_name = ''

    def get_next_task(self):
        if not session.get('current_task_name'):
            current_task_index = 0
        else:
            print('in get next')
            print(session['current_task_name'])
            current_task_index = self.task_list_names.index(session['current_task_name'])
            print(current_task_index)
            current_task_index += 1
        print(f"Going to: {current_task_index}")
        print(f"Its name is {self.task_list_names[current_task_index]}")
        print(self.task_block_list[current_task_index])
        session['current_task_name'] = self.task_list_names[current_task_index]
        return self.task_block_list[current_task_index].get_starting_route()


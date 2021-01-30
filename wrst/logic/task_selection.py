# This files contains the code to deal with how to pick the next task for a given user
# Content exists in a database
# User starts with a random task and moves sequentially from there
# User will loop upon reaching the last task in the queue, and will continue until having completed all tasks (or timeout)

from flask import session, Markup, request
from wrst.database import db
from wrst.database.models import User, Relationship, Tasks
from sqlalchemy import and_, or_, func
from wrst.logic.experiment import Experiment
from wrst.forms.wrst_forms import (
    FamilyForm,
    AllFamilyForm,
    EntityEntityForm,
    EntityEventForm,
    EventEventForm,
    TaxonomyForm,
    ComponentForm,
    SpatialForm,
    FunctionalForm,
    CausalForm,
    ParticipantForm,
    EventStructureForm,
    FinalSubmitForm,
)

import pandas as pd
import numpy as np
import re

all_forms = [
    FamilyForm,
    EntityEntityForm,
    EntityEventForm,
    EventEventForm,
    TaxonomyForm,
    ComponentForm,
    SpatialForm,
    FunctionalForm,
    EventStructureForm,
    CausalForm,
    ParticipantForm,
]

def get_text_dynamic():

    # Check to see if the user has finished all available tasks . . . if so route to completion screen
    num_tasks_available = db.session.query(func.max(Tasks.task_id)).first()[0]
    num_tasks_completed = db.session.query(Relationship).filter(Relationship.user==session["user_id"]).count()
    if num_tasks_completed >= num_tasks_available:
        print("User has finished everything")
        # Do something to signal the calling function that this person is done and route accordingly
        return (-1, "", "", "", "", "", "", "", "", "")
    elif num_tasks_completed==0:
        current_task_id = np.random.choice(num_tasks_available)
    else:
        last_task_id = session["current_task_id"]
        #last_id = db.session.query(func.max(Relationship.id)).filter(Relationship.user==session["user_id"]).first()[0]
        #last_task_id = db.session.query(Relationship.task_id).filter(Relationship.id==last_id).first()[0]
        current_task_id = (last_task_id + 1) % num_tasks_available

    # NEW EXPERIMENTAL SCARY SHIT
    session["current_task_id"] = current_task_id

    print("Current task id: {}".format(current_task_id))
    # Get the actual task info given the current_task_id
    task = db.session.query(Tasks).filter(Tasks.task_id==current_task_id).first()
    sentence_id = task.sentence_id
    content_url = session["reading_link"]
    term_1 = task.term_1
    term_2 = task.term_2
    type_1 = task.type_1
    type_2 = task.type_2
    base_term_1 = task.base_term_1
    base_term_2 = task.base_term_2
    terms = [term_1, term_2]
    content = task.sentence
    for t in terms:
        t = t.replace('(', '\(').replace(')', '\)')
        pattern = re.compile(t, re.IGNORECASE)
        content = pattern.sub(
            '<span style="background-color: #FFFF00">{}</span>'.format(t),
            content,
            1,
        )
        print(content)
        content = content.replace('\(', '(').replace('\)', ')')
    content = "<h3>{}</h3>".format(content)
    question_text = "What type of relationship exists between {} and {}?".format(
        term_1, term_2
    )
    types = [type_1, type_2]
    N_entity = sum([t == "entity" for t in types])
    N_event = sum([t == "event" for t in types])
    if N_entity == 2:  # entity-entity relationship
        family_form_name = "entity_entity"
    elif N_entity == 1:  # entity-event relationship
        family_form_name = "entity_event"
    else:  # event-event relationship
        family_form_name = "event_event"

    return (
        current_task_id,
        sentence_id,
        term_1,
        term_2,
        base_term_1,
        base_term_2,
        type_1,
        type_2,
        family_form_name,
        content,
        question_text,
        content_url,
    )


def get_next_form_by_ref(form):

    # Prep the set of keys that correspond to valid form selections
    keys = list(form.button_keys)

    # Iterate over the valid form keys and return the stringified form name if there is a match
    for ii, label in enumerate(keys):
        if getattr(form, label).data:
            return form.form_link_names[ii]

    # Default behavior in case something gets messed up . . .
    return AllFamilyForm.name


def get_form_by_name(form_name):
    for form in all_forms:
        print(form_name)
        if form.name == form_name:
            return form(request.form)

    # Default form in case something gets messed up
    print("Iz bad")
    return AllFamilyForm(request.form)

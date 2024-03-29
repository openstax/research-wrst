from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User, Relationship, Tasks
import time
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
    TextInputForm
)
from wrst.logic.decorators import login_required
from wrst.logic.task_selection import get_text_dynamic, get_next_form_by_ref, get_form_by_name
import numpy as np
from wrst.forms.wrst_forms import NONE_OF_THE_ABOVE_TEXT
wrst_routes = Blueprint('wrst_routes', __name__)
import datetime
from wrst.logic.experiment import task_queue

MAX_RELATIONSHIP_LENGTH = 30

def auto_flip_terms(family_category, term_1, term_2, base_term_1, base_term_2, type_1, type_2):
    # Logic goes here
    if family_category == 'functional': # Order will be entity->event
        if type_1 == 'event': # It's not right, so flip it
            tmp_term = term_1
            tmp_base = base_term_1
            tmp_type = type_1
            term_1 = term_2
            base_term_1 = base_term_2
            type_1 = type_2
            term_2 = tmp_term
            base_term_2 = tmp_base
            type_2 = tmp_type
    elif family_category == 'participant': # Order will be event->entity
        if type_1 == 'entity': # It's not right, so flip it
            tmp_term = term_1
            tmp_base = base_term_1
            tmp_type = type_1
            term_1 = term_2
            base_term_1 = base_term_2
            type_1 = type_2
            term_2 = tmp_term
            base_term_2 = tmp_base
            type_2 = tmp_type
    else: # If we ever need to handle some other case . . .
        pass

    return term_1, term_2, base_term_1, base_term_2, type_1, type_2

def log_relationship(user,
                     task_id,
                     paragraph_id,
                     term_1,
                     term_2,
                     base_term_1,
                     base_term_2,
                     family,
                     relationship,
                     family_id_time,
                     relationship_id_time,
                     total_time
                     ):
    new_relationship = Relationship(
        user=user,
        task_id=task_id,
        paragraph_id=paragraph_id,
        term_1=term_1,
        term_2=term_2,
        base_term_1=base_term_1,
        base_term_2=base_term_2,
        family=family,
        relationship=relationship,
        family_id_time=family_id_time,
        relationship_id_time=relationship_id_time,
        total_time=total_time,
        task_completion_time=datetime.datetime.now()
    )
    db.session.add(new_relationship)
    db.session.commit()

def make_time_str(t):
    t_str = "0 min."
    if (t<60):
        t_str = '{} sec.'.format(int(np.floor(t)))
    elif (t>60) and (t<3600):
        t_str = '{} min. {} sec.'.format(int(np.floor(t/60)), int(t % 60))
    elif (t>=3600):
        t_str = '{} hr. {} min.'.format(int(np.floor(t/3600)), int(np.floor((t % 3600)/60)))
    return t_str




@wrst_routes.route('/get_new_task', methods=['GET', 'POST'])
@login_required
def get_new_task():

    # Get the next task details
    current_task_id, paragraph_id, term_1, term_2, base_term_1, base_term_2, type_1, type_2, family_form_name, content, question_text, content_url = get_text_dynamic()

    # print("In GNT")
    # print(family_form_name)

    # Reset the timing session variables
    session['family_time_on_task'] = 0
    session['relationship_time_on_task'] = 0
    session['current_task_id'] = current_task_id

    # Get the current total time-on-task value for the user
    user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    relationship_completion_times = db.session.query(Relationship.total_time).filter(Relationship.user==session['user_id']).all()
    total_time_on_task = float(np.sum(relationship_completion_times))

    session['total_time_on_task'] = make_time_str(total_time_on_task)

    # Check if user has completed the required amount of time
    # If so, send to completion page
    required_time_on_task = session['required_time_on_task']
    # print("Time comp")
    # print(total_time_on_task)
    # print(required_time_on_task)
    if (required_time_on_task < total_time_on_task) or (current_task_id==-1):
        print("We have a stop condition!")
        if current_task_id==-1:
            print("End of task")
        else:
            print("Timeout")
        return redirect(url_for('instruction_routes.generic_reroute'))
            # return redirect(url_for('instruction_routes.instruction_final'))
    else:
        return redirect(url_for('wrst_routes.do_wrst_family',
                                paragraph_id=paragraph_id,
                                content=content,
                                question_text=question_text,
                                term_1=term_1,
                                term_2=term_2,
                                base_term_1=base_term_1,
                                base_term_2=base_term_2,
                                type_1=type_1,
                                type_2=type_2,
                                family_form_name=family_form_name,
                                user_email=session['user_id'],
                                content_url=content_url
                                )
                        )


@wrst_routes.route('/family', methods=['GET', 'POST'])
@login_required
def do_wrst_family():
    # Unpack the data
    paragraph_id = request.args["paragraph_id"]
    term_1 = request.args["term_1"]
    term_2 = request.args["term_2"]
    type_1 = request.args["type_1"]
    type_2 = request.args["type_2"]
    base_term_1 = request.args["base_term_1"]
    base_term_2 = request.args["base_term_2"]
    family_form_name = request.args["family_form_name"]
    content = Markup(request.args["content"])
    question_text = request.args["question_text"]
    content_url = request.args["content_url"]

    # Load the form
    form = get_form_by_name(family_form_name)
    # form = FamilyForm(request.form)  # Old default


    if not form.validate_on_submit():

        # Set a new session start time
        session["last_family_start_time"] = time.time()

        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               type_1="",
                               type_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str=session['total_time_on_task'],
                               content_url=content_url)
    if request.method == 'POST':

        # Test out the form stuff:
        return_text = get_next_form_by_ref(form)
        # print("OUTPUT: {}".format(return_text))

        # Update the family selection time-on-task
        session["family_time_on_task"] += (time.time() - session["last_family_start_time"])
        # print(session["family_time_on_task"])

        # Route to the relationship selection task if a suitable option was chosen
        if return_text not in ["no_relationship", "dont_know", "text_input"]:
            return redirect(url_for('wrst_routes.do_wrst_relationship',
                                    form_title=return_text,
                                    family_form_name=family_form_name,
                                    paragraph_id=paragraph_id,
                                    content=content,
                                    question_text=question_text,
                                    term_1=term_1,
                                    term_2=term_2,
                                    base_term_1=base_term_1,
                                    base_term_2=base_term_2,
                                    type_1=type_1,
                                    type_2=type_2,
                                    user_email=session['user_id'],
                                    content_url=content_url
                                    )
                            )
        elif 'text_input' in return_text:
            return redirect(url_for('wrst_routes.do_text_submission',
                                    form_title=return_text,
                                    family_form_name=family_form_name,
                                    paragraph_id=paragraph_id,
                                    content=content,
                                    question_text=question_text,
                                    family_category="NA",
                                    term_1=term_1,
                                    term_2=term_2,
                                    base_term_1=base_term_1,
                                    base_term_2=base_term_2,
                                    type_1=type_1,
                                    type_2=type_2,
                                    user_email=session['user_id'],
                                    content_url=content_url
                                    )
                            )
        else:
            # User chose an non-relational option, just log that
            log_relationship(
                user=session["user_id"],
                task_id=session["current_task_id"],
                paragraph_id=paragraph_id,
                term_1=term_1,
                term_2=term_2,
                base_term_1=base_term_1,
                base_term_2=base_term_2,
                family=return_text,
                relationship="NA",
                family_id_time=session['family_time_on_task'],
                relationship_id_time=session["relationship_time_on_task"],
                total_time=session['family_time_on_task'] + session["relationship_time_on_task"]
            )
            return redirect(url_for('wrst_routes.get_new_task'))


@wrst_routes.route('/relationship', methods=['GET', 'POST'])
@login_required
def do_wrst_relationship():

    # Unpack the data from the family form
    form_title = request.args["form_title"]
    family_form_name = request.args["family_form_name"]
    paragraph_id = request.args["paragraph_id"]
    family_category = form_title
    content = Markup(request.args["content"])
    question_text = request.args["question_text"]
    term_1 = request.args["term_1"]
    term_2 = request.args["term_2"]
    base_term_1 = request.args["base_term_1"]
    base_term_2 = request.args["base_term_2"]
    type_1 = request.args["type_1"]
    type_2 = request.args["type_2"]
    content_url = request.args["content_url"]

    form = get_form_by_name(form_title)

    # print(f"THE FAMILY CATEGORY IS {family_category}")
    term_1, term_2, base_term_1, base_term_2, type_1, type_2 = auto_flip_terms(family_category,
                                                                               term_1,
                                                                               term_2,
                                                                               base_term_1,
                                                                               base_term_2,
                                                                               type_1,
                                                                               type_2)

    # Calculate the padding on the terms
    # Number of (buttons + 2) x some height
    Nb = len(form.button_keys) + 2
    term_padding = Nb * 20

    if not form.validate_on_submit():
        # Set a new session start time
        session["last_relationship_start_time"] = time.time()

        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text="Select the relationship that best applies",
                               term_1=term_1,
                               term_2=term_2,
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               term_padding=term_padding,
                               user_email=session['user_id'],
                               time_on_task_str=session['total_time_on_task'],
                               content_url=content_url)

    if request.method == 'POST':
        # Update the family selection time-on-task
        session["relationship_time_on_task"] += (time.time() - session["last_relationship_start_time"])
        # print(session["relationship_time_on_task"])

        # Check to see if we have pressed either the flip or back buttons
        if form.flip_relationship.data:
            # Just re-render the template with the terms inverted
            return redirect(url_for('wrst_routes.do_wrst_relationship',
                                    form_title=form_title,
                                    family_form_name=family_form_name,
                                    paragraph_id=paragraph_id,
                                    content=content,
                                    question_text=question_text,
                                    term_1=term_2,
                                    term_2=term_1,
                                    base_term_1=base_term_2,
                                    base_term_2=base_term_1,
                                    type_1=type_1,
                                    type_2=type_2,
                                    user_email=session['user_id'],
                                    content_url=content_url)
                            )
        elif form.go_back_button.data:
            return redirect(url_for('wrst_routes.do_wrst_family',
                                    paragraph_id=paragraph_id,
                                    content=content,
                                    question_text=question_text,
                                    term_1=term_1,
                                    term_2=term_2,
                                    base_term_1=base_term_1,
                                    base_term_2=base_term_2,
                                    type_1=type_1,
                                    type_2=type_2,
                                    family_form_name=family_form_name,
                                    user_email=session['user_id'],
                                    content_url=content_url
                                    )
                            )
        else:
            # The user has selected a relationship
            # So we need to get which one they selected and route to final submission page
            for key in form.button_keys:
                if form[key].data:
                    relationship = form.button_dict[key]

            if relationship != NONE_OF_THE_ABOVE_TEXT:
                return redirect(url_for('wrst_routes.submission',
                                        paragraph_id=paragraph_id,
                                        content=content,
                                        question_text=question_text,
                                        term_1=term_1,
                                        term_2=term_2,
                                        base_term_1=base_term_1,
                                        base_term_2=base_term_2,
                                        type_1=type_1,
                                        type_2=type_2,
                                        family_form_name=family_form_name,
                                        family_category=family_category,
                                        relationship=relationship,
                                        user_email=session['user_id'],
                                        content_url=content_url
                                        )
                                )
            else:
                return redirect(url_for('wrst_routes.do_text_submission',
                                        form_title=relationship,
                                        family_form_name=family_form_name,
                                        paragraph_id=paragraph_id,
                                        content=content,
                                        question_text=question_text,
                                        family_category=family_category,
                                        term_1=term_1,
                                        term_2=term_2,
                                        base_term_1=base_term_1,
                                        base_term_2=base_term_2,
                                        type_1=type_1,
                                        type_2=type_2,
                                        user_email=session['user_id'],
                                        content_url=content_url
                                        )
                                )

@wrst_routes.route('/submission', methods=['GET', 'POST'])
@login_required
def submission():
    # Unpack the data from the relationship form
    paragraph_id = request.args["paragraph_id"]
    content = Markup(request.args["content"])
    term_1 = request.args["term_1"]
    term_2 = request.args["term_2"]
    base_term_1 = request.args["base_term_1"]
    base_term_2 = request.args["base_term_2"]
    type_1 = request.args["type_1"]
    type_2 = request.args["type_2"]
    family_form_name = request.args["family_form_name"]
    family_category = request.args["family_category"]
    relationship = request.args["relationship"]
    question_text = request.args["question_text"]
    content_url = request.args["content_url"]

    form = FinalSubmitForm(request.form)
    # Render form if we need to
    if not form.validate_on_submit():
        # Set a new session start time
        session["last_relationship_start_time"] = time.time()

        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text="You selected: {} {} {}".format(term_1, relationship, term_2),
                               term_1="",
                               term_2="",
                               user_email=session['user_id'],
                               time_on_task_str=session['total_time_on_task'],
                               content_url=content_url)

    if request.method == 'POST':
        # Update the family selection time-on-task
        session["relationship_time_on_task"] += (time.time() - session["last_relationship_start_time"])

        # Check to see if we have pressed either the flip or back buttons
        if form.go_back_button.data:
            return redirect(url_for('wrst_routes.do_wrst_family',
                                    paragraph_id=paragraph_id,
                                    content=content,
                                    question_text=question_text,
                                    term_1=term_1,
                                    term_2=term_2,
                                    base_term_1=base_term_1,
                                    base_term_2=base_term_2,
                                    type_1=type_1,
                                    type_2=type_2,
                                    family_form_name=family_form_name,
                                    user_email=session['user_id'],
                                    content_url=content_url
                                    )
                            )
        else:
            # The user has selected a relationship
            # So we need to get which one they selected and route to final submission page
            log_relationship(
                user=session["user_id"],
                task_id=session["current_task_id"],
                paragraph_id=paragraph_id,
                term_1=term_1,
                term_2=term_2,
                base_term_1=base_term_1,
                base_term_2=base_term_2,
                family=family_category,
                relationship=relationship,
                family_id_time=session['family_time_on_task'],
                relationship_id_time=session["relationship_time_on_task"],
                total_time=session['family_time_on_task'] + session["relationship_time_on_task"],
            )

            # Route back to get_new_task
            return redirect(url_for('wrst_routes.get_new_task'))

@wrst_routes.route('/do_text_submission', methods=['GET', 'POST'])
@login_required
def do_text_submission():

    # Unpack the data from the relationship form
    paragraph_id = request.args["paragraph_id"]
    content = Markup(request.args["content"])
    term_1 = request.args["term_1"]
    term_2 = request.args["term_2"]
    base_term_1 = request.args["base_term_1"]
    base_term_2 = request.args["base_term_2"]
    type_1 = request.args["type_1"]
    type_2 = request.args["type_2"]
    family_form_name = request.args["family_form_name"]
    question_text = request.args["question_text"]
    content_url = request.args["content_url"]
    family_category = request.args["family_category"]

    form = TextInputForm(request.form)
    # Render form if we need to
    if not form.validate_on_submit():
        # Set a new session start time
        session["last_relationship_start_time"] = time.time()

        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text="Type in the relationship that you think applies",
                               term_1="",
                               term_2="",
                               user_email=session['user_id'],
                               time_on_task_str=session['total_time_on_task'],
                               content_url=content_url)

    if request.method == 'POST':
        # Update the family selection time-on-task
        session["relationship_time_on_task"] += (time.time() - session["last_relationship_start_time"])


        relationship = request.form.get('text')
        if (len(relationship) > MAX_RELATIONSHIP_LENGTH):
            relationship = relationship[0:MAX_RELATIONSHIP_LENGTH]

        # Check to see if we have pressed either the flip or back buttons
        if form.go_back_button.data:
            return redirect(url_for('wrst_routes.do_wrst_family',
                                    paragraph_id=paragraph_id,
                                    content=content,
                                    question_text=question_text,
                                    term_1=term_1,
                                    term_2=term_2,
                                    base_term_1=base_term_1,
                                    base_term_2=base_term_2,
                                    type_1=type_1,
                                    type_2=type_2,
                                    family_form_name=family_form_name,
                                    user_email=session['user_id'],
                                    content_url=content_url
                                    )
                            )
        else:
            # The user has submitted things
            # Get the text from the textbox
            # That will be the "relationship"
            log_relationship(
                user=session["user_id"],
                task_id=session["current_task_id"],
                paragraph_id=paragraph_id,
                term_1=term_1,
                term_2=term_2,
                base_term_1=base_term_1,
                base_term_2=base_term_2,
                family=family_category,
                relationship=relationship,
                family_id_time=session['family_time_on_task'],
                relationship_id_time=session["relationship_time_on_task"],
                total_time=session['family_time_on_task'] + session["relationship_time_on_task"],
            )

            # Route back to get_new_task
            return redirect(url_for('wrst_routes.get_new_task'))

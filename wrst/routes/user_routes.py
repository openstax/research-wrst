from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User
from wrst.logic.experiment import ProlificExperiment, PsychExperiment, TestExperiment, task_queue
from wrst.forms.user_forms import UserLogin, UserCreation, UserEdit
import string
import numpy as np
import datetime

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['GET', 'POST'])
def splash_page():
    # Check if the user is currently logged in via a session variable. If so, route to task. Else, to login
    if session.get('email_address', None):
        return redirect(url_for('wrst_routes.do_wrst_family'))
    else:
        return redirect(url_for('user_routes.login_prolific')) 
    # This will need to be updated for prolific 
    #    return redirect(url_for('user_routes.login_test'))


# TODO: Assign cohort based on current number of participants
@user_routes.route('/login_prolific', methods=['GET', 'POST'])
def login_prolific():

    experiment = ProlificExperiment()
    user_id = request.args["PROLIFIC_PID"]
    session_id = request.args["SESSION_ID"]
    study_id = request.args["STUDY_ID"]
    study_name = 'prolific'
    prolific_cohorts = db.session.query(User.study_cohort).filter(User.study_name=='prolific')
    N_a = len([c for c in prolific_cohorts if c=='a'])
    # N_b = len([c for c in prolific_cohorts if c == 'b']) # COMMENT OUT BEFORE PUSHING
    cohort = 'a' 
    # if (N_a > N_b): # COMMENT OUT BEFORE PUSHING
    #     cohort = 'b' # COMMENT OUT BEFORE PUSHING

    consent_text = """Before beginning the study, you need to know your rights as a research participant. Please read the following consent form, and indicate whether you consent to participate. Note, you can scroll in the box to view the entire consent form."""

    # If we are creating/logging in a new user clear out the session
    session_keys = list(session.keys())
    print(session_keys)
    if '_permanent' in session_keys:
        session_keys.remove('_permanent')
    if 'csrf_token' in session_keys:
        session_keys.remove('csrf_token')
    for key in session_keys:
        session.pop(key)

    cohort_idx = experiment.cohort_names.index(cohort)
    session['required_time_on_task'] = experiment.task_time
    session['required_reading_time'] = experiment.reading_time
    session['reading_link'] = experiment.reading_links[cohort_idx]

    form = UserCreation(request.form)
    if not form.validate_on_submit():
        return render_template('user_create.html',
                               main_message="Convergence Accelerator Study",
                               secondary_message=consent_text,
                               form=form)

    if request.method == 'POST':

        # If user consented, add them to db and route to instructions page
        if form.create_agree_button.data:
            new_user = User(user_id=user_id,
                            study_name=study_name,
                            study_cohort=cohort,
                            required_time_on_task_seconds=session['required_time_on_task'],
                            required_reading_time_seconds=session['required_reading_time'],
                            user_creation_time=datetime.datetime.now()
                            )
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = user_id
            session['session_id'] = session_id
            session['study_id'] = study_id
            return redirect(url_for('instruction_routes.generic_reroute'))
        else:
            return redirect(url_for('instruction_routes.consent_not_provided'))

# TODO: Assign cohort based on current number of participants
@user_routes.route('/login_psych', methods=['GET', 'POST'])
def login_psych():

    experiment = PsychExperiment()
    if "USER_ID" not in request.args:
        return "Need to provide valid USER_ID field"
    elif "COHORT" not in request.args:
        return "Need to provide valid COHORT field"

    user_id = request.args["USER_ID"]
    cohort = request.args["COHORT"]
    cohort_idx = experiment.cohort_names.index(cohort)
    study_name = 'psych'

    # If we are creating/logging in a new user clear out the session
    session_keys = list(session.keys())
    if '_permanent' in session_keys:
        session_keys.remove('_permanent')
    if 'csrf_token' in session_keys:
        session_keys.remove('csrf_token')
    for key in session_keys:
        session.pop(key)

    session['required_time_on_task'] = experiment.task_time
    session['required_reading_time'] = experiment.reading_time
    session['reading_link'] = experiment.reading_links[cohort_idx]

    new_user = User(user_id=user_id,
                    study_name=study_name,
                    study_cohort=cohort,
                    required_time_on_task_seconds=session['required_time_on_task'],
                    required_reading_time_seconds=session['required_reading_time'],
                    user_creation_time=datetime.datetime.now()
                    )
    db.session.add(new_user)
    db.session.commit()

    session['user_id'] = user_id
    return redirect(url_for('instruction_routes.generic_reroute'))


# TODO: Assign cohort based on current number of participants
@user_routes.route('/login_test', methods=['GET', 'POST'])
def login_test():

    experiment = TestExperiment()
    consent_text = """Before beginning the study, you need to know your rights as a research participant. Please read the following consent form, and indicate whether you consent to participate. Note, you can scroll in the box to view the entire consent form."""

    letters_nums = list(string.ascii_lowercase) + [0,1,2,3,4,5,6,7,8,9]
    user_id = ''.join(np.random.choice(letters_nums, 10, replace=True).tolist())
    cohort_idx = 1*(np.random.rand()>0)
    cohort = experiment.cohort_names[cohort_idx]
    study_name = 'test'

    # If we are creating/logging in a new user clear out the session
    session_keys = list(session.keys())
    if '_permanent' in session_keys:
        session_keys.remove('_permanent')
    if 'csrf_token' in session_keys:
        session_keys.remove('csrf_token')
    for key in session_keys:
        session.pop(key)

    session['required_time_on_task'] = experiment.task_time
    session['required_reading_time'] = experiment.reading_time
    session['reading_link'] = experiment.reading_links[cohort_idx]

    form = UserCreation(request.form)
    if not form.validate_on_submit():
        return render_template('user_create.html',
                               main_message="Convergence Accelerator Study",
                               secondary_message=consent_text,
                               form=form)

    if request.method == 'POST':

        # If user consented, add them to db and route to instructions page
        if form.create_agree_button.data:
            new_user = User(user_id=user_id,
                            study_name=study_name,
                            study_cohort=cohort,
                            required_time_on_task_seconds=session['required_time_on_task'],
                            required_reading_time_seconds=session['required_reading_time'],
                            user_creation_time=datetime.datetime.now()
                            )
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = user_id
            # TODO: Put this back test dear god don't forget this
            return redirect(url_for('instruction_routes.generic_reroute'))
        else:
            return redirect(url_for('instruction_routes.consent_not_provided'))


@user_routes.route('/logout', methods=['GET', 'POST'])
def logout():

    # Remove all session variables for the user
    session.clear()

    # Reroute back to the main login page
    return "You logged out!"



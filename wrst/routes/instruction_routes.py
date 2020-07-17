from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User, Relationship
from wrst.logic.decorators import login_required
from wrst.logic.experiment import ProlificExperiment, task_queue
from wrst.forms.instruction_forms import InstructionForm

instruction_routes = Blueprint('instruction_routes', __name__)

@instruction_routes.route('/display_task_instructions', methods=['GET', 'POST'])
@login_required
def display_task_instructions():
    # Load the form
    form = InstructionForm(request.form)
    header = "Convergence Accelerator Study"
    content_items = Markup("""<p>In this study, you first read a section from an introductory Biology textbook for 5 minutes. <br><br>
                    After reading the text, you will step through a training activity. The training activity will teach you how to label the relationships between the biology concepts you just read about. The training will last approximately 5 minutes. <br><br>
                    After the training exercise, you will then label the relationships between biology terms. The relationship task will last 30 minutes. <br><br>
                    When you are ready to begin, press next.<br></p>
                    """)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        return redirect(url_for('instruction_routes.generic_reroute'))
        # return redirect(url_for('reading_routes.display_reading_instructions'))

@instruction_routes.route('/consent_not_provided', methods=['GET', 'POST'])
def consent_not_provided():
    form = InstructionForm(request.form)
    header = "Without providing consent, you will not be eligible to participate in the study. If this was a mistake, hit the back button on your browser to give consent."
    content_items = Markup("<p></p>")


    return render_template('instruction_pages.html',
                            form=form,
                            instruction_header=header,
                            content_items=content_items,
                            obscure_form=True)



@instruction_routes.route('/instruction_final', methods=['GET', 'POST'])
@login_required
def instruction_final():

    # The user has finished the training, so mark training as complete
    user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    user.task_complete = True
    db.session.commit()

    # Get the study name and route accordingly
    study_name = user.study_name
    print("Study name: {}".format(study_name))

    if study_name == 'prolific':
        return redirect(url_for('instruction_routes.prolific_final')
                        )
    else:
        return redirect(url_for('instruction_routes.psych_final')
                        )

@instruction_routes.route('/prolific_final', methods=['GET', 'POST'])
@login_required
def prolific_final():

    print(f"At the end with user {session['user_id']}")
    user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    user.task_complete = True
    db.session.commit()

    form = InstructionForm(request.form)
    header = "You have finished the task!"
    content_items = Markup(
        """
        <p> Thank you so much for all of your time! Click the 'Next' button to get routed back to Prolific
        and get your completion logged.</p>
        """
    )
    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    else:

        experiment = ProlificExperiment()
        prolific_url_final = experiment.redirect_link        
        return redirect(prolific_url_final)


@instruction_routes.route('/psych_final', methods=['GET', 'POST'])
@login_required
def psych_final():

    form = InstructionForm(request.form)
    header = "You have finished the task!"
    content_items = Markup(
        """
        <p> Thank you so much for all of your time! Contact the research coordinator for further instructions.</p>
        """
    )
    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               obscure_form=True)


@instruction_routes.route('/generic_reroute', methods=['GET', 'POST'])
@login_required
def generic_reroute():
    if 'distractor_seconds' in session:
        session.pop('distractor_seconds')
    print(f"Back in generic reroute with user {session['user_id']}")
    route = task_queue.get_next_task()
    return redirect(route)

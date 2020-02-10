from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.logic.decorators import login_required
from wrst.forms.instruction_forms import InstructionForm

instruction_routes = Blueprint('instruction_routes', __name__)

@instruction_routes.route('/display_task_instructions', methods=['GET', 'POST'])
@login_required
def display_task_instructions():
    # Load the form
    form = InstructionForm(request.form)
    header = "Convergence Accelerator Study"
    content_items = Markup("""<p>In this study, you first read a section from an introductory Biology textbook for 10 minutes. <br><br>
                    After reading the text, you will step through a training activity. The training activity will teach you how to label the relationships between the biology concepts you just read about. The training will last approximately 5 minutes. <br><br>
                    After the training exercise, you will then label the relationships between biology terms. The relationship task will last 25 minutes. <br><br>
                    When you are ready to begin, press next.<br></p>
                    """)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('reading_routes.display_reading_instructions')

                        )
@instruction_routes.route('/consent_not_provided', methods=['GET', 'POST'])
def consent_not_provided():
    form = InstructionForm(request.form)
    header = "Without providing consent, you will not be eligible to participate in the study. If this was a mistake, hit the back button on your browser to give consent."
    content_items = Markup("<p></p>")

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('user_routes.create_user'))

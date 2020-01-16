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
    header = "Welcome to the WRST Activity Ever! Here is a quick rundown of what you will be doing:"
    content_items = [
        "You will complete a brief reading of a section in an introductory Biology textbook (10 minutes)",
        "You will complete a brief training on concept mapping -- which is deciding how various terms relate together (approx 5 minutes)",
        "You will complete some concept mapping exercises on the content that you read (25 minutes)"
    ]
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('reading_routes.display_reading_instructions')
                        )

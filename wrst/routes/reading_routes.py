from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.logic.decorators import login_required
from wrst.forms.reading_forms import ReadingForm
import time
from wrst.logic.experiment import task_queue

reading_routes = Blueprint('reading_routes', __name__)

# TODO: Make reading link dynamic based on cohort
@reading_routes.route('/display_reading_instructions', methods=['GET', 'POST'])
@login_required
def display_reading_instructions():

    total_reading_time = session['required_reading_time']

    # Load the form
    form = ReadingForm(request.form)
    reading_link = session["reading_link"]
    header = "You are now going to read a brief section from an introductory Biology textbook"
    content_items = Markup(
        """<p>During this portion of the study, please read the text that is linked at the bottom of this page. Don't worry about memorizing all of the information. Just try get a general familiarity with the topic to the best of your ability.<br><br>
        Please spend at least 15 minutes reading the text. We have provided a timer on this page to help you keep track. <br><br>
        When the timer expires, you can click on the 'Next' button to move to the next step of the activity.<br></p>
        """
    )
    content = Markup(header)

    if not form.validate_on_submit():

        if not session.get('reading_start_time'):
            session['reading_start_time'] = time.time()

        current_time_reading = time.time() - session['reading_start_time']

        return render_template('reading_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               reading_link=reading_link,
                               num=total_reading_time-current_time_reading)
    if request.method == 'POST':

        # Verify that the user has spent the required reading time
        # If so, they can pass on
        current_time_reading = time.time() - session['reading_start_time']
        if (current_time_reading>=total_reading_time):
            return redirect(url_for('instruction_routes.generic_reroute'))
        else:
            flash("You need to spend at least ten minutes reading before moving on to the next activity!")
            return redirect(url_for('reading_routes.display_reading_instructions')
                            )
        # Else, flash a message and re-render the page

from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.logic.decorators import login_required
from wrst.forms.reading_forms import ReadingForm
import time

reading_routes = Blueprint('reading_routes', __name__)

# TODO: Make reading link dynamic based on cohort
@reading_routes.route('/display_reading_instructions', methods=['GET', 'POST'])
@login_required
def display_reading_instructions():

    total_reading_time = 30 # seconds

    # Load the form
    form = ReadingForm(request.form)
    reading_link = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
    header = "First, you are going to read a brief section from an introductory Biology textbook"
    content_items = [
        "We want you to spend at least 10 minutes reading this text. We have provided a timer on this page to help you keep track.",
        "Don't worry about trying to memorize all of the information.  Just try to get a general familiarity with the topic to the best of your ability.",
        "When the timer expires, you can click on the 'Next' button to move to next step of the activity",
        "Click the link below to access the reading material (it will open in a separate tab).",
        "Note, for testing we have just reduced the time to 30 seconds -- will change before deployment"
    ]
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
            return redirect(url_for('training_routes.training_1')
                            )
        else:
            flash("You need to spend at least ten minutes reading before moving on to the next activity!")
            return redirect(url_for('reading_routes.display_reading_instructions')
                            )
        # Else, flash a message and re-render the page

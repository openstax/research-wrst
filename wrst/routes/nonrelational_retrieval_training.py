from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User, Relationship
import time
from wrst.forms.wrst_forms import EntityEntityForm, TaxonomyForm, ComponentForm, SpatialForm, FunctionalForm, FinalSubmitForm, TextInputForm
from wrst.forms.instruction_forms import InstructionForm
from wrst.logic.decorators import login_required
from wrst.logic.experiment import ProlificExperiment

retrieval_training_routes = Blueprint('retrieval_training_routes', __name__)

@retrieval_training_routes.route('/retrieval_training_1', methods=['GET', 'POST'])
@login_required
def retrieval_training_1():

    form = InstructionForm(request.form)
    header = "Retrieval Training"
    content_items = Markup(
        """<p>
        Planning how you study will allow you to use your time efficiently and maximize what 
        you will remember later. <b>Retrieval</b>, or the practice of recalling information you have 
        learned without receiving any hints, is extremely effective at helping students remember 
        information over the long-term. However, many students use less effective strategies to study, 
        such as re-reading the same information over and over. 
        </p>
        """
    )
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.retrieval_training_2')
                        )

@retrieval_training_routes.route('/retrieval_training_2', methods=['GET', 'POST'])
@login_required
def retrieval_training_2():

    form = InstructionForm(request.form)
    header = "Retrieval Training"
    content_items = Markup(
        """<p>
        Retrieval practice requires more cognitive effort than other techniques, 
        but that is also what makes it so effective. Studying should create “desirable difficulties” 
        for students to maximize their retention.
        </p>
        """
    )
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.retrieval_training_3')
                        )


@retrieval_training_routes.route('/retrieval_training_3', methods=['GET', 'POST'])
@login_required
def retrieval_training_3():

    form = InstructionForm(request.form)
    header = "Retrieval Training"
    content_items = Markup(
        """<p>
        Research consistently shows that for the same amount of time, 
        <b>reading the material once + retrieval practice is more effective than re-reading the entire time.</b>
        </p>
        """
    )

    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.changing_habits_1')
                        )

@retrieval_training_routes.route('/retrieval_training_routes.changing_habits_1', methods=['GET', 'POST'])
@login_required
def changing_habits_1():

    form = InstructionForm(request.form)
    header = "Changing Your Study Habits"
    content_items = Markup(
        """<p>
        Research shows that even when students are taught (and believe) that practicing retrieval 
        is more effective than re-studying, they often still do not practice retrieval. 
        Students must use retrieval practice <b>intentionally and repeatedly</b> until they are in the 
        habit of practicing retrieval every time they study.
        </p>
        """
    )
    images = [
             ]
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               )
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.practicing_retrieval_1')
                        )

@retrieval_training_routes.route('/practicing_retrieval_1', methods=['GET', 'POST'])
@login_required
def practicing_retrieval_1():

    form = InstructionForm(request.form)
    header = "Practicing Retrieval"
    content_items = Markup(
        """<p>
        Retrieval practice requires that you recall information more than once each study session. 
        Many students, even if they quiz themselves or use flashcards, consider the information 
        “learned” if they retrieve it once in a session and only use retrieval practice to determine their 
        progress in memorizing information.
        </p>
        """
    )
    images = [
              ['practicing_retrieval.png', ''],
             ]
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.practicing_retrieval_2')
                        )

@retrieval_training_routes.route('/practicing_retrieval_2', methods=['GET', 'POST'])
@login_required
def practicing_retrieval_2():

    form = InstructionForm(request.form)
    header = "Practicing Retrieval"
    content_items = Markup(
        """<p>
        To be most effective, retrieving information <b>three times per study session</b> is a good goal. 
        </p>
        """
    )
    images = [
              ['practicing_retrieval.png', ''],
             ]
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.learn_new_material_1')
                        )


@retrieval_training_routes.route('/learn_new_material_1', methods=['GET', 'POST'])
@login_required
def learn_new_material_1():

    form = InstructionForm(request.form)
    header = "How to Learn New Material"
    content_items = Markup(
        """<p>
        Study new material <b>once</b>. Do not re-read anything, even if all the content is new to you. Then begin practicing retrieval.
 
        </p>
        """
    )
    images = [
             ]
    content = Markup(header)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.learn_new_material_2')
                        )


@retrieval_training_routes.route('/learn_new_material_2', methods=['GET', 'POST'])
@login_required
def learn_new_material_2():
    form = InstructionForm(request.form)
    header = "How to Learn New Material"
    content_items = Markup(
        """<p>
        If you are studying on your own, quiz yourself. 
        Do not look at the text for the correct until you’ve produced an answer on your own. 
        If you are using flashcards or taking a quiz, do not look at the answer until you have thought 
        through the question and selected a response on your own. 
        <b>Students often confuse familiarity with a concept with knowing the correct answer.</b> 
        Take a few extra seconds to commit to an answer for yourself, and only then check the correct answer. 
        You might not know the answer as well as you thought.
        </p>
        """
    )
    images = [
    ]
    content = Markup(header)

    if not form.validate_on_submit():
        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.monitor_1')
                        )

@retrieval_training_routes.route('/monitor_1', methods=['GET', 'POST'])
@login_required
def monitor_1():
    form = InstructionForm(request.form)
    header = "Monitor Your Learning"
    content_items = Markup(
        """<p>
        The key to successful retrieval learning is <b>monitoring your performance</b>. 
        First, know that you will likely get many or most items wrong at first. 
        Do not let that deter you from continuing with the strategy. 
        Students tend to confuse perceived difficulty with an indication that their study technique is not working. 
        The cognitive effort will be worthwhile, and retrieval practice works.
        </p>
        """
    )
    images = [
        ['monitor_learning.png', '']
    ]
    content = Markup(header)

    if not form.validate_on_submit():
        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.monitor_2')
                        )

@retrieval_training_routes.route('/monitor_2', methods=['GET', 'POST'])
@login_required
def monitor_2():
    form = InstructionForm(request.form)
    header = "Monitor Your Learning"
    content_items = Markup(
        """<p>
        Second, pay attention to the <b>accuracy</b> of your responses by checking for the correct answer 
        after you practice retrieval every time, even if you’re certain you know the correct answer. 
        Note whether your accuracy is increasing over time.
        </p>
        """
    )
    images = [
        ['monitor_learning.png', '']
    ]
    content = Markup(header)

    if not form.validate_on_submit():
        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('retrieval_training_routes.monitor_3')
                        )

@retrieval_training_routes.route('/monitor_3', methods=['GET', 'POST'])
@login_required
def monitor_3():
    form = InstructionForm(request.form)
    header = "Monitor Your Learning"
    content_items = Markup(
        """<p>
        Third, keep track of <b>how many times</b> you have practiced retrieving that content. 
        Until you have retrieved an answer successfully three times, you should keep recalling the 
        information whenever you have the opportunity. 
        </p>
        """
    )
    images = [
        ['monitor_learning.png', '']
    ]
    content = Markup(header)

    if not form.validate_on_submit():
        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('instruction_routes.generic_reroute')
                        )

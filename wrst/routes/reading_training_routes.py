from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User, Relationship
import time
from wrst.forms.wrst_forms import EntityEntityForm, TaxonomyForm, ComponentForm, SpatialForm, FunctionalForm, FinalSubmitForm, TextInputForm
from wrst.forms.instruction_forms import InstructionForm
from wrst.logic.decorators import login_required
from wrst.logic.experiment import ProlificExperiment

reading_training_routes = Blueprint('reading_training_routes', __name__)

@reading_training_routes.route('/reading_training_1', methods=['GET', 'POST'])
@login_required
def reading_training_1():

    form = InstructionForm(request.form)
    header = "Reading Strategies Training"
    content_items = Markup(
        """<p>
        Before you begin reading, think about your <b>goals</b>. What are you trying to achieve by reading a certain text? 
        For example, are you trying to understand a topic in depth, memorize concepts for an exam, or get a general 
        idea of a subject you’re interested in? Knowing your goals will help you focus your attention and effort.<br><br>

        Next, consider how using reading strategies can be personally <b>useful</b> to you. Many students do not automatically 
        apply reading strategies, but certain strategies can be very useful. This particular study will only involve 
        one text, but you can apply reading strategies to anything else you read in your life, which will help you 
        learn faster and retain your knowledge longer. You will be more likely to retain these reading strategies if 
        you believe they are useful. 

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

        return redirect(url_for('reading_training_routes.reading_training_before_you_start')
                        )

@reading_training_routes.route('/reading_training_before_you_start', methods=['GET', 'POST'])
@login_required
def reading_training_before_you_start():

    form = InstructionForm(request.form)
    header = "Before You Start Reading"
    content_items = Markup(
        """<p>
        First (before you begin reading the text fully), use the <b>preview strategy</b> to get the “big picture” of the topic 
        of the reading assignment. Look at headings, subheadings, bolded words, and the first sentences in each section 
        to give you clues about what is most important in the text. 
        </p>
        """
    )
    images = [
              ['reading_main.png', ''],
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

        return redirect(url_for('reading_training_routes.monitor_understanding')
                        )

@reading_training_routes.route('/monitor_understanding', methods=['GET', 'POST'])
@login_required
def monitor_understanding():

    form = InstructionForm(request.form)
    header = "While Reading"
    content_items = Markup(
        """<p>
        As you read, you should <b>monitor your understanding</b> of the content. Ask yourself how much of the text you are 
        comprehending and how much of a knowledge gap you have between what you are reading about and what you already 
        knew. Are you making progress toward meeting your original reading goal? If you do not know a word, can you use 
        context clues to guess what it means? Having difficulties does not mean you should stop reading! Slow down and 
        read more slowly when you reach difficult sections, and pause to think about what you just read. Your reading 
        skills will grow as you continue to challenge yourself.
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

        return redirect(url_for('reading_training_routes.reading_training_evaluate')
                        )

@reading_training_routes.route('/reading_training_evaluate', methods=['GET', 'POST'])
@login_required
def reading_training_evaluate():

    form = InstructionForm(request.form)
    header = "While Reading"
    content_items = Markup(
        """<p>
        You should also evaluate the text as you read it. Who wrote the content? Why did they write it, and are there 
        multiple purposes the text could serve? What kind of audience did the author intend to read it? What purpose 
        does reading it serve you? Answering these questions will help you process and retain the information that you 
        read.
        </p>
        """
    )
    images = [
              ['reading_evaluate.png', ''],
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

        return redirect(url_for('reading_training_routes.reading_training_keyword_strategy')
                        )

@reading_training_routes.route('/reading_training_keyword_strategy', methods=['GET', 'POST'])
@login_required
def reading_training_keyword_strategy():

    form = InstructionForm(request.form)
    header = "While Reading"
    content_items = Markup(
        """<p>
        The <b>keyword</b> strategy involves mentally assigning a “keyword” to each paragraph or section of text after you 
        read the section, generally using a keyword the text actually contains. Create a mental image of this keyword 
        once you have selected it, and then expand your mental image with other information in that text section.
        </p>
        """
    )
    images = [
              ['reading_keyword.png', ''],
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

        return redirect(url_for('reading_training_routes.reading_training_mental_imagery')
                        )

@reading_training_routes.route('/reading_training_mental_imagery', methods=['GET', 'POST'])
@login_required
def reading_training_mental_imagery():

    form = InstructionForm(request.form)
    header = "While Reading"
    content_items = Markup(
        """<p>
        <b>Mental imagery</b> is also a tool that can also be used on its own. Spend time to create a mental image of what you 
        are reading, using any figures or photographs included with the text for guides. As you read more and learn 
        more details, either expand upon that mental image, or build a second mental image. 

        </p>
        """
    )
    images = [
              ['reading_mental.png', ''],
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

        return redirect(url_for('reading_training_routes.reading_training_after_reading')
                        )

@reading_training_routes.route('/reading_training_after_reading', methods=['GET', 'POST'])
@login_required
def reading_training_after_reading():

    form = InstructionForm(request.form)
    header = "After Reading"
    content_items = Markup(
        """<p>
        In some cases, re-reading is a useful strategy. You do not need to <b>re-read</b> the entire text. Re-reading 
        is most effective when you focus on the sections you struggled with the most. Go slowly and pause if you need 
        to as you re-read difficult passages.
        </p>
        """
    )
    images = [
              ['reading_after.png', ''],
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

        return redirect(url_for('reading_training_routes.reading_training_maximizing_retention')
                        )

@reading_training_routes.route('/reading_training_maximizing_retention', methods=['GET', 'POST'])
@login_required
def reading_training_maximizing_retention():

    form = InstructionForm(request.form)
    header = "Maximizing Your Retention for Exams"
    content_items = Markup(
        """<p>
        Overall, reading to maximize your retention should involve some cognitive effort. By paying attention to not 
        only <i>what</i> you are reading but <i>how</i> you are reading, and coming up with strategies like mental images, you will 
        be building a deeper understanding of the topic. The deeper you understand something, the better you will 
        retain that information long-term, and the better prepared you will be to be tested on it later.
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

        return redirect(url_for('instruction_routes.generic_reroute')
                        )

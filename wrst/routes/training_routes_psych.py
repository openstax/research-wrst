from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User, Relationship
import time
from wrst.forms.wrst_forms import EntityEntityForm, TaxonomyForm, EntityEventForm, CausalForm, EventEventForm, ComponentForm, SpatialForm, FunctionalForm, FinalSubmitForm, TextInputForm
from wrst.forms.instruction_forms import InstructionForm
from wrst.logic.decorators import login_required
from wrst.logic.experiment import ProlificExperiment

training_routes_psych = Blueprint('training_routes_psych', __name__)

@training_routes_psych.route('/training_1_psych', methods=['GET', 'POST'])
@login_required
def training_1_psych():

    form = InstructionForm(request.form)
    header = "Relationship selection: Training"
    content_items = Markup(
        """<p>In the next portion of this study, you will be identifying how the different psychology concepts you just
        read about are related. Before you begin, we will walk you through a brief training. <br><br>
        During the relationships selection task, you will be shown two terms. Your job will be to identify the relationship 
        that exists between the terms (if there is one).<br><br>
        There are a LOT of possible relationships available and so, to make this easier, we have broken the task up into two parts: </p>
        <ul>
        <li>First, you will select a high-level relationship family</li>
        <li>Second, you will select the specific relationship within the family that you have chosen</li>
        </ul>
        <br>
        <p>DON'T FEEL LIKE YOU NEED TO MEMORIZE ALL THE RELATIONSHIPS! There will be reminders in the task to help you 
        if you get stuck.<br></p>
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

        return redirect(url_for('training_routes_psych.training_1b_psych')
                        )

@training_routes_psych.route('/training_1b_psych', methods=['GET', 'POST'])
@login_required
def training_1b_psych():

    form = InstructionForm(request.form)
    header = "Entities vs Events"
    content_items = Markup("""
    <p> There are two kinds of terms that you will link: Entities and Events. <br><br>
    <ul>
    <li>Entities correspond to actual things (like cats, tables, cells, etc)</li>
    <li>Events correspond to things that happen (like falling, starting a car, mitosis, etc)</li>
    </ul>
    """)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_taxonomic_psych'))


@training_routes_psych.route('/training_taxonomic_psych', methods=['GET', 'POST'])
@login_required
def training_taxonomic_psych():

    form = InstructionForm(request.form)
    header = "Taxonomic Relationship Family (Entity to Entity)"
    content_items = Markup("<p>These relationships describe how types of one entity relate to other entities</p>")
    images = [
              ['type_of.png', 'Type relationships relationships define subclasses of an entity'],
              ['instance_of.png', 'Instance relationship define specific occurences of a entity']
             ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_component_psych')
                        )

@training_routes_psych.route('/training_component_psych', methods=['GET', 'POST'])
@login_required
def training_component_psych():

    form = InstructionForm(request.form)
    header = "Component Family (Entity to Entity)"
    content_items = Markup("<p>These relationships describe how some entities are made of up other entities</p>")
    images = [
        ['contains.png', 'Contains denotes that an entity contains some other entity'],
        ['has_part.png', 'Material relationships denote when an underlying material makes up an entity']
    ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_spatial_psych')
                        )

@training_routes_psych.route('/training_spatial_psych', methods=['GET', 'POST'])
@login_required
def training_spatial_psych():

    form = InstructionForm(request.form)
    header = "Spatial Relationships (Entity to Entity)"
    content_items = Markup("<p>These relationships describe how entities are located around other entities</p>")
    images = [
        ['resides_against.png', 'For entities that are next to each other'],
        ['is_above.png', 'An entity resides above another entity'],
        ['is_inside.png', 'An entity resides inside another entity']
    ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_functional_psych')
                        )

@training_routes_psych.route('/training_functional_psych', methods=['GET', 'POST'])
@login_required
def training_functional_psych():

    form = InstructionForm(request.form)
    header = "Functional Relationships (Entity to Event)"
    content_items = Markup("<p>These relationships describe how entities are located around other entities</p>")
    images = [
        ['has_function.png', 'The function of one entity is some event (A hammer nails things)'],
        ['facilitates.png', 'An entity facilitates some function (the hammerhead facilitates the nailing)']
    ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_causal_psych')
                        )

@training_routes_psych.route('/training_causal_psych', methods=['GET', 'POST'])
@login_required
def training_causal_psych():

    form = InstructionForm(request.form)
    header = "Causal Relationships (Event to Event)"
    content_items = Markup("<p>These relationships describe how events cause other events</p>")
    images = [
        ['key_starts_car.png', 'Turning the key causes the car to start'],
        ['car_accelerating.png', 'Pushing on the gas enables motion'],
        ['car_braking.png', 'Pushing on the brake inhibits motion'],
        ['car_boot.png', 'A boot on the tire prevents motion']
    ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_event_structure_psych')
                        )

@training_routes_psych.route('/training_event_structure_psych', methods=['GET', 'POST'])
@login_required
def training_event_structure_psych():

    form = InstructionForm(request.form)
    header = "Event Structure Relationships (Event to Event)"
    content_items = Markup(
        """<p>These relationships describe when events occur with respect to other events.<br><br>
        Consider the example of how to boil potatoes:<br></p>
        """)
    images = [
        ['boiling_water.jpeg', 'Step 1: Put pot of water on stove to boil (first event)'],
        ['cut_potatoes.jpeg', 'Step 2: While the water boils, cut up the potatoes (subevent)'],
        ['potatoes_water.jpeg', 'Step 3: After the water boils, add the potatoes (next event)'],
    ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_participant_psych')
                        )
@training_routes_psych.route('/training_participant_psych', methods=['GET', 'POST'])
@login_required
def training_participant_psych():

    form = InstructionForm(request.form)
    header = "Participant Relationships (Entity to Event)"
    content_items = Markup(
        """<p>These relationships describe how entities participate in events.<br><br>
        The cat pushed the vase with it's paw. The vase broke on the ground into many pieces.<br></p>
        """)

    images = [
        ['cat_push_vase.png', 'The cat pushed the vase (participants)'],
        ['cat_uses_paw.png', "The cat used it's paw (instrument)"],
        ['vase_ground.png', 'The vase landed on the ground (site)'],
        ['broken_vase.png', 'The vase broke into many pieces (result)']
    ]

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items,
                               images=images)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_no_direct_psych'))


@training_routes_psych.route('/training_no_direct_psych', methods=['GET', 'POST'])
@login_required
def training_no_direct_psych():

    form = InstructionForm(request.form)
    header = "No Direct Relationships"
    content_items = Markup(
        """<p>Often (maybe most of the time) terms won't have a direct relationship.<br><br>
        Ex: The cat is on the table. The dog is outside ==> the cat and dog have no direct relationship.<br><br>
        Ex: The table has legs. The legs are plastic ==> the table and plastic are related through the legs, but not directly related to each other<br></p>
        """)

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_7_psych')
                        )

@training_routes_psych.route('/training_7_psych', methods=['GET', 'POST'])
@login_required
def training_7_psych():

    form = EventEventForm(request.form)
    content = '<h3>For an individual to experience <span style="background-color: #FFFF00">stress</span>, he must first encounter a <span style="background-color: #FFFF00">potential stressor</span></term></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("potential stressor", "stress")
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash("This is an example screen")
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               next_arrow=True,
                               next_link=url_for('training_routes_psych.training_8_psych'))


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_8_psych')
                        )

@training_routes_psych.route('/training_8_psych', methods=['GET', 'POST'])
@login_required
def training_8_psych():

    form = EventEventForm(request.form)
    content = '<h3>For an individual to experience <span style="background-color: #FFFF00">stress</span>, he must first encounter a <span style="background-color: #FFFF00">potential stressor</span></term></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("potential stressor", "stress")
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash("On the left is the content pane. You will have the selected text with the two terms highlighted.  There is also a link to the original textbook if you think that will be helpful.")
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               next_arrow=True,
                               next_link=url_for('training_routes_psych.training_9_psych')
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_9_psych')
                        )

@training_routes_psych.route('/training_9_psych', methods=['GET', 'POST'])
@login_required
def training_9_psych():

    form = EventEventForm(request.form)
    content = '<h3>For an individual to experience <span style="background-color: #FFFF00">stress</span>, he must first encounter a <span style="background-color: #FFFF00">potential stressor</span></term></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("potential stressor", "stress")
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash("On the right is the relationship selection pane. You can click on one of the buttons to choose a relationship family or (later) a specific relationship. You can hover your mouse over any of the buttons to get a reminder of what each relationship entails.")
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               next_arrow=True,
                               next_link=url_for('training_routes_psych.training_10_psych',
                                                 flash_message="Our first task is to pick the relationship family that relates these terms.  Since the text talks about the potential stressors causing stress we should pick the 'causal' relationship family")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_10_psych',
                                flash_message="Our first task is to pick the relationship family that relates these terms.  Since the text talks about the potential stressors causing stress we should pick the 'causal' relationship family")
                        )

@training_routes_psych.route('/training_10_psych', methods=['GET', 'POST'])
@login_required
def training_10_psych():

    flash_message = request.args["flash_message"]
    form = EventEventForm(request.form)
    content = '<h3>For an individual to experience <span style="background-color: #FFFF00">stress</span>, he must first encounter a <span style="background-color: #FFFF00">potential stressor</span></term></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("potential stressor", "stress")
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url)


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit1.data:  # Causal relationship is submit1
            return redirect(url_for('training_routes_psych.training_11_psych', flash_message="Good job! Now we need to select the correct subclass relationship from the new list. Here we would choose 'is inside of' on the right.")
                        )
        else:
            return redirect(url_for('training_routes_psych.training_10_psych', flash_message="This is a causal relationship so click on that button to continue on.")
                        )

@training_routes_psych.route('/training_11_psych', methods=['GET', 'POST'])
@login_required
def training_11_psych():

    flash_message = request.args["flash_message"]
    form = CausalForm(request.form)
    content = '<h3>For an individual to experience <span style="background-color: #FFFF00">stress</span>, he must first encounter a <span style="background-color: #FFFF00">potential stressor</span></term></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("potential stressor", "stress")
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    Nb = len(form.button_keys) + 2
    term_padding = Nb * 20

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="potential stressor",
                               term_2="stress",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               term_padding=term_padding,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url)


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit0.data:  # 'causes' is submit1 for the causal form
            return redirect(url_for('training_routes_psych.training_12_psych', flash_message="Now we are at the final submission page.  We get to review the relationship we have chosen and make changes if we need to.  We are looking good so click that option!")
                        )
        else:
            return redirect(url_for('training_routes_psych.training_11_psych', flash_message="The correct relationship is 'causes'. Click that button to continue.")
                            )

@training_routes_psych.route('/training_12_psych', methods=['GET', 'POST'])
@login_required
def training_12_psych():

    flash_message = request.args["flash_message"]
    form = FinalSubmitForm(request.form)
    content = '<h3>For an individual to experience <span style="background-color: #FFFF00">stress</span>, he must first encounter a <span style="background-color: #FFFF00">potential stressor</span></term></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("potential stressor", "stress")
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    # content_url = "https://archive.cnx.org/contents/8d50a0af-948b-4204-a71d-4826cba765b8@15.1:2ec76ad2-c275-4b81-9168-244ef063caee@13"
    term_1 = "potential stressor"
    term_2 = "stress"
    relationship = "causes"
    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text="You selected: {} {} {}".format(term_1, relationship, term_2),
                               term_1="",
                               term_2="",
                               user_email=session['user_id'],
                               time_on_task_str="0 min.",
                               content_url=content_url)



    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit.data:  # 'is inside of' is submit2 for the spatial form
            return redirect(url_for('training_routes_psych.training_13_psych', flash_message="Here is another example. Let's start by picking the best relationship family for these two terms.")
                        )
        else:
            return redirect(url_for('training_routes_psych.training_12_psych', flash_message="We are happy with this relationship, so click on the 'Submit Selection' option")
                            )

@training_routes_psych.route('/training_13_psych', methods=['GET', 'POST'])
@login_required
def training_13_psych():

    form = EntityEntityForm(request.form)
    term_1 = "stressor"
    term_2 = "acute"
    content = '<h3>In general, <span style="background-color: #FFFF00">stressors</span> can be placed into one of two broad categories: chronic and <span style="background-color: #FFFF00">acute</span>.</h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"
    flash_message = request.args["flash_message"]

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit0.data:
            return redirect(url_for('training_routes_psych.training_14_psych',
                                    flash_message="Good job! Now we need to pick the correct taxonomic relationship.  There is a problem, though.  The term order seems backwards. Click the 'Flip Relationship' button to change the order.")
                            )
        else:
            return redirect(url_for('training_routes_psych.training_13_psych',
                                    flash_message="That's not right -- the text is describing a class-oriented relationship, which is under the 'Taxonomic' category.  Click that one.")
                            )


@training_routes_psych.route('/training_14_psych', methods=['GET', 'POST'])
@login_required
def training_14_psych():

    form = TaxonomyForm(request.form)
    term_1 = "stressor"
    term_2 = "acute"
    content = '<h3>In general, <span style="background-color: #FFFF00">stressors</span> can be placed into one of two broad categories: chronic and <span style="background-color: #FFFF00">acute</span>.</h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"
    flash_message = request.args["flash_message"]
    Nb = len(form.button_keys) + 2
    term_padding = Nb * 20

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1=term_1,
                               term_2=term_2,
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               term_padding=term_padding,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.flip_relationship.data:
            return redirect(url_for('training_routes_psych.training_15_psych',
                                    flash_message="Fantastic! Now the term order makes sense and we can choose the final relationship.")
                            )
        else:
            return redirect(url_for('training_routes_psych.training_14_psych',
                                    flash_message="The term order is important for this relationship to make sense.  Click 'Flip Relationship' to get it right")
                            )

@training_routes_psych.route('/training_15_psych', methods=['GET', 'POST'])
@login_required
def training_15_psych():

    form = TaxonomyForm(request.form)
    term_1 = "acute"
    term_2 = "stressor"
    content = '<h3>In general, <span style="background-color: #FFFF00">stressors</span> can be placed into one of two broad categories: chronic and <span style="background-color: #FFFF00">acute</span>.</h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"
    flash_message = request.args["flash_message"]
    Nb = len(form.button_keys) + 2
    term_padding = Nb * 20

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1=term_1,
                               term_2=term_2,
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               term_padding=term_padding,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit0.data:
            return redirect(url_for('training_routes_psych.training_16_psych',
                                    flash_message="Excellent! Now we can just submit to finalize")
                            )
        else:
            return redirect(url_for('training_routes_psych.training_15_psych',
                                    flash_message="That's not right -- acute is a specific type of stressor. Pick that relationship.")
                            )

@training_routes_psych.route('/training_16_psych', methods=['GET', 'POST'])
@login_required
def training_16_psych():

    flash_message = request.args["flash_message"]
    form = FinalSubmitForm(request.form)
    term_1 = "acute"
    term_2 = "stressor"
    content = '<h3>In general, <span style="background-color: #FFFF00">stressors</span> can be placed into one of two broad categories: chronic and <span style="background-color: #FFFF00">acute</span></h3>.'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"
    flash_message = request.args["flash_message"]
    relationship = "is a type of"
    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text="You selected: {} {} {}".format(term_1, relationship, term_2),
                               term_1="",
                               term_2="",
                               user_email=session['user_id'],
                               time_on_task_str="0 min.",
                               content_url=content_url)



    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit.data:  # 'is inside of' is submit2 for the spatial form
            return redirect(url_for('training_routes_psych.training_17_psych', flash_message="Let's do one last task. What relationship do you think exists between these two terms?")
                        )
        else:
            return redirect(url_for('training_routes_psych.training_16_psych', flash_message="Everything here is correct so we can submit to finalize."))


@training_routes_psych.route('/training_17_psych', methods=['GET', 'POST'])
@login_required
def training_17_psych():

    form = EntityEntityForm(request.form)
    term_1 = "extreme"
    term_2 = "chronic"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>When stress is <span style="background-color: #FFFF00">extreme</span> or <span style="background-color: #FFFF00">chronic</span>, it can have profoundly negative consequences.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"
    flash_message = request.args["flash_message"]
    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               )



    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit3.data:  # 'no relationship' is submit3 for the spatial form
            return redirect(url_for('training_routes_psych.training_18_psych', flash_message="Excellent job! While there definitely are connections between extreme stress and chronic stress they are not *directly* related.")
                        )
        else:
            return redirect(url_for('training_routes_psych.training_17_psych', flash_message="This isn't the right relationship for this term pair.  Let's try another one"))

@training_routes_psych.route('/training_18_psych', methods=['GET', 'POST'])
@login_required
def training_18_psych():
    form = EntityEntityForm(request.form)
    term_1 = "extreme"
    term_2 = "chronic"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>When stress is <span style="background-color: #FFFF00">extreme</span> or <span style="background-color: #FFFF00">chronic</span>, it can have profoundly negative consequences.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"
    flash_message = request.args["flash_message"]

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               next_arrow=True,
                               next_link=url_for('training_routes_psych.training_text_submission_1_psych', flash_message="There is one last relationship option that we want to discuss: creating your own relationships!")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_text_submission_1_psych', flash_message="There is one last relationship option that we want tp discuss: creating your own relationships!"))


@training_routes_psych.route('/training_text_submission_1_psych', methods=['GET', 'POST'])
@login_required
def training_text_submission_1_psych():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "participants"
    term_2 = "items"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>In developing their scale, Holmes and Rahe asked 394 <span style="background-color: #FFFF00">participants</span> to provide a numerical estimate for each of the 43 <span style="background-color: #FFFF00">items<span></h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               next_arrow=True,
                               next_link=url_for('training_routes_psych.training_text_submission_2_psych', flash_message="If two terms are related, but none of the relationship buttons seem quite right, you can enter your own.")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_text_submission_2_psych', flash_message="If two terms are related, but none of the relationship buttons seem quite right, you can enter your own."))

@training_routes_psych.route('/training_text_submission_2_psych', methods=['GET', 'POST'])
@login_required
def training_text_submission_2_psych():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "participants"
    term_2 = "items"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>In developing their scale, Holmes and Rahe asked 394 <span style="background-color: #FFFF00">participants</span> to provide a numerical estimate for each of the 43 <span style="background-color: #FFFF00">items<span></h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url,
                               next_arrow=True,
                               next_link=url_for('training_routes_psych.training_text_submission_3_psych',
                                                 flash_message="Try clicking on the 'Define new relationship button'")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes_psych.training_text_submission_3_psych', flash_message="Try clicking on the 'Define new relationship button'"))

@training_routes_psych.route('/training_text_submission_3_psych', methods=['GET', 'POST'])
@login_required
def training_text_submission_3_psych():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "participants"
    term_2 = "items"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>In developing their scale, Holmes and Rahe asked 394 <span style="background-color: #FFFF00">participants</span> to provide a numerical estimate for each of the 43 <span style="background-color: #FFFF00">items<span></h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="",
                               term_2="",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url
                               )


    if request.method == 'POST':
        # Make sure they hit the right button
            if form.submit5.data:  # 'Define' is submit4 on entity-entity
                return redirect(url_for('training_routes_psych.training_text_submission_4_psych',
                                        flash_message="Now you have a text box on the right. Type in some text and click 'Submit'")
                                )
            else:
                return redirect(url_for('training_routes_psych.training_text_submission_3_psych',
                                        flash_message="Click on the 'Define a new relationship' button to move on"))

@training_routes_psych.route('/training_text_submission_4_psych', methods=['GET', 'POST'])
@login_required
def training_text_submission_4_psych():
    flash_message = request.args["flash_message"]
    form = TextInputForm(request.form)
    term_1 = "participants"
    term_2 = "items"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>In developing their scale, Holmes and Rahe asked 394 <span style="background-color: #FFFF00">participants</span> to provide a numerical estimate for each of the 43 <span style="background-color: #FFFF00">items<span></h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/psychology-2e/pages/14-2-stressors"

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text="Type in the relationship that you think applies",
                               term_1="",
                               term_2="",
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url)

    if request.method == 'POST':
        # Make sure they hit the right button
            if form.submit.data:  # 'Define' is submit4 on entity-event
                return redirect(url_for('training_routes_psych.training_19_psych'))
            else:
                return redirect(url_for('training_routes_psych.training_text_submission_4_psych',
                                        flash_message="Type some text and click on the 'Submit' button to move on"))

@training_routes_psych.route('/training_19_psych', methods=['GET', 'POST'])
@login_required
def training_19_psych():

    # The user has finished the training, so mark training as complete
    user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    user.training_complete = True
    db.session.commit()


    form = InstructionForm(request.form)
    header = "You have finished the training modules!"
    content_items = Markup(
        """
        <p>You will now be moved on to create your own relationships on new content. <br><br>
        You will spend 30 minutes on these tasks.  There is a timer in the upper right hand corner to show you how
        long you have spent thus far. <br><br>
        Remember that you can always hover your mouse over the relationship choices to get a reminder on what they mean. <br><br>
        Finally, you can always chose the 'I don't know' button to get a new example if you get stuck on one example.<br>
        </p>
        """
    )

    if not form.validate_on_submit():

        return render_template('instruction_pages.html',
                               form=form,
                               instruction_header=header,
                               content_items=content_items)
    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('instruction_routes.generic_reroute'))
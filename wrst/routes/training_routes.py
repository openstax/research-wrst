from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User, Relationship
import time
from wrst.forms.wrst_forms import EntityEntityForm, TaxonomyForm, ComponentForm, SpatialForm, FunctionalForm, FinalSubmitForm, TextInputForm
from wrst.forms.instruction_forms import InstructionForm
from wrst.logic.decorators import login_required
from wrst.logic.experiment import ProlificExperiment

training_routes = Blueprint('training_routes', __name__)

@training_routes.route('/training_1', methods=['GET', 'POST'])
@login_required
def training_1():

    form = InstructionForm(request.form)
    header = "Relationship selection: Training"
    content_items = Markup(
        """<p>In the next portion of this study, you will be identifying how the different biology concepts you just
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

        return redirect(url_for('training_routes.training_1b')
                        )

@training_routes.route('/training_1b', methods=['GET', 'POST'])
@login_required
def training_1b():

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

        return redirect(url_for('training_routes.training_taxonomic'))


@training_routes.route('/training_taxonomic', methods=['GET', 'POST'])
@login_required
def training_taxonomic():

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

        return redirect(url_for('training_routes.training_component')
                        )

@training_routes.route('/training_component', methods=['GET', 'POST'])
@login_required
def training_component():

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

        return redirect(url_for('training_routes.training_spatial')
                        )

@training_routes.route('/training_spatial', methods=['GET', 'POST'])
@login_required
def training_spatial():

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

        return redirect(url_for('training_routes.training_functional')
                        )

@training_routes.route('/training_functional', methods=['GET', 'POST'])
@login_required
def training_functional():

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

        return redirect(url_for('training_routes.training_causal')
                        )

@training_routes.route('/training_causal', methods=['GET', 'POST'])
@login_required
def training_causal():

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

        return redirect(url_for('training_routes.training_event_structure')
                        )

@training_routes.route('/training_event_structure', methods=['GET', 'POST'])
@login_required
def training_event_structure():

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

        return redirect(url_for('training_routes.training_participant')
                        )
@training_routes.route('/training_participant', methods=['GET', 'POST'])
@login_required
def training_participant():

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

        return redirect(url_for('training_routes.training_no_direct'))


@training_routes.route('/training_no_direct', methods=['GET', 'POST'])
@login_required
def training_no_direct():

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

        return redirect(url_for('training_routes.training_7')
                        )

@training_routes.route('/training_7', methods=['GET', 'POST'])
@login_required
def training_7():

    form = EntityEntityForm(request.form)
    content = '<h3>The <span style="background-color: #FFFF00">nucleus</span> resides inside the <span style="background-color: #FFFF00">cytoplasm</span></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("cytoplasm", "nucleus")
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                               next_link=url_for('training_routes.training_8'))


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes.training_8')
                        )

@training_routes.route('/training_8', methods=['GET', 'POST'])
@login_required
def training_8():

    form = EntityEntityForm(request.form)
    content = '<h3>The <span style="background-color: #FFFF00">nucleus</span> resides inside the <span style="background-color: #FFFF00">cytoplasm</span></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("cytoplasm", "nucleus")
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                               next_link=url_for('training_routes.training_9')
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes.training_9')
                        )

@training_routes.route('/training_9', methods=['GET', 'POST'])
@login_required
def training_9():

    form = EntityEntityForm(request.form)
    content = '<h3>The <span style="background-color: #FFFF00">nucleus</span> resides inside the <span style="background-color: #FFFF00">cytoplasm</span></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("cytoplasm", "nucleus")
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                               next_link=url_for('training_routes.training_10',
                                                 flash_message="Our first task is to pick the relationship family that relates these terms.  Since the text talks about the nucleus being inside the cytoplasm we should pick the 'spatial' relationship family")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes.training_10',
                                flash_message="Our first task is to pick the relationship family that relates these terms.  Since the text talks about the nucleus being inside the cytoplasm we should pick the 'spatial' relationship family")
                        )

@training_routes.route('/training_10', methods=['GET', 'POST'])
@login_required
def training_10():

    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    content = '<h3>The <span style="background-color: #FFFF00">nucleus</span> resides inside the <span style="background-color: #FFFF00">cytoplasm</span></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("cytoplasm", "nucleus")
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
        if form.submit2.data:  # Spatial relationship is submit2
            return redirect(url_for('training_routes.training_11', flash_message="Good job! Now we need to select the correct relationship from the list. Note the order of the terms -- we want to select 'is inside of' since cytoplasm comes first")
                        )
        else:
            return redirect(url_for('training_routes.training_10', flash_message="This is a spatial relationship so click on that button to continue on.")
                        )

@training_routes.route('/training_11', methods=['GET', 'POST'])
@login_required
def training_11():

    flash_message = request.args["flash_message"]
    form = SpatialForm(request.form)
    content = '<h3>The <span style="background-color: #FFFF00">nucleus</span> resides inside the <span style="background-color: #FFFF00">cytoplasm</span></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("cytoplasm", "nucleus")
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

    Nb = len(form.button_keys) + 2
    term_padding = Nb * 20

    if not form.validate_on_submit():
        flash(flash_message)
        return render_template('wrst_pages.html',
                               form=form,
                               textbook_content=content,
                               question_text=question_text,
                               term_1="nucleus",
                               term_2="cytoplasm",
                               button_keys=form.button_keys,
                               hovertext=form.hovertext,
                               term_padding=term_padding,
                               user_email=session['user_id'],
                               time_on_task_str="0 sec",
                               content_url=content_url)


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"
        if form.submit2.data:  # 'is inside of' is submit2 for the spatial form
            return redirect(url_for('training_routes.training_12', flash_message="Now we are at the final submission page.  We get to review the relationship we have chosen and make changes if we need to.  We are looking good so click that option!")
                        )
        else:
            return redirect(url_for('training_routes.training_11', flash_message="The correct relationship is 'is inside of'. Click that button to continue.")
                            )

@training_routes.route('/training_12', methods=['GET', 'POST'])
@login_required
def training_12():

    flash_message = request.args["flash_message"]
    form = FinalSubmitForm(request.form)
    content = '<h3>The <span style="background-color: #FFFF00">nucleus</span> resides inside the <span style="background-color: #FFFF00">cytoplasm</span></h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format("cytoplasm", "nucleus")
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
    # content_url = "https://archive.cnx.org/contents/8d50a0af-948b-4204-a71d-4826cba765b8@15.1:2ec76ad2-c275-4b81-9168-244ef063caee@13"
    term_1 = "nucleus"
    term_2 = "cytoplasm"
    relationship = "is inside of"
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
            return redirect(url_for('training_routes.training_13', flash_message="Here is another example. Let's start by picking the best relationship family for these two terms.")
                        )
        else:
            return redirect(url_for('training_routes.training_12', flash_message="We are happy with this relationship, so click on the 'Looks good!' option")
                            )

@training_routes.route('/training_13', methods=['GET', 'POST'])
@login_required
def training_13():

    form = EntityEntityForm(request.form)
    term_1 = "cell"
    term_2 = "eukaryotic"
    content = '<h3>The <span style="background-color: #FFFF00">Cells</span> fall into one of two broad categories: prokaryotic and <span style="background-color: #FFFF00">eukaryotic</span>. We classify only the predominantly single-cells organisms Bacteria and Archaea as prokaryotes (pro- = “before”; -kary- = “nucleus”). Animal cells, plants, fungi, and protists are all eukaryotes (eu- = “true”)</h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
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
            return redirect(url_for('training_routes.training_14',
                                    flash_message="Good job! Now we need to pick the correct taxonomic relationship.  There is a problem, though.  The term order seems backwards. Click the 'Flip Relationship' button to change the order.")
                            )
        else:
            return redirect(url_for('training_routes.training_13',
                                    flash_message="That's not right -- the text is describing a class-oriented relationship, which is under the 'Taxonomic' cateogory.  Click that one.")
                            )


@training_routes.route('/training_14', methods=['GET', 'POST'])
@login_required
def training_14():

    form = TaxonomyForm(request.form)
    term_1 = "cell"
    term_2 = "eukaryotic"
    content = '<h3>The <span style="background-color: #FFFF00">Cells</span> fall into one of two broad categories: prokaryotic and <span style="background-color: #FFFF00">eukaryotic</span>. We classify only the predominantly single-cells organisms Bacteria and Archaea as prokaryotes (pro- = “before”; -kary- = “nucleus”). Animal cells, plants, fungi, and protists are all eukaryotes (eu- = “true”)</h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
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
            return redirect(url_for('training_routes.training_15',
                                    flash_message="Fantastic! Now the term order makes sense and we can choose the final relationship.")
                            )
        else:
            return redirect(url_for('training_routes.training_14',
                                    flash_message="The term order is important for this relationship to make sense.  Click 'Flip Relationship' to get it right")
                            )

@training_routes.route('/training_15', methods=['GET', 'POST'])
@login_required
def training_15():

    form = TaxonomyForm(request.form)
    term_1 = "eukaryotic"
    term_2 = "cell"
    content = '<h3>The <span style="background-color: #FFFF00">Cells</span> fall into one of two broad categories: prokaryotic and <span style="background-color: #FFFF00">eukaryotic</span>. We classify only the predominantly single-cells organisms Bacteria and Archaea as prokaryotes (pro- = “before”; -kary- = “nucleus”). Animal cells, plants, fungi, and protists are all eukaryotes (eu- = “true”)</h3>'
    content = Markup(content)
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
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
            return redirect(url_for('training_routes.training_16',
                                    flash_message="Rocking! Now we can just submit to finalize")
                            )
        else:
            return redirect(url_for('training_routes.training_15',
                                    flash_message="That's not right -- the eukaryotic is a specific type of cell. Pick that relationship.")
                            )

@training_routes.route('/training_16', methods=['GET', 'POST'])
@login_required
def training_16():

    flash_message = request.args["flash_message"]
    form = FinalSubmitForm(request.form)
    term_1 = "eukaryotic"
    term_2 = "cell"
    content = '<h3>The <span style="background-color: #FFFF00">Cells</span> fall into one of two broad categories: prokaryotic and <span style="background-color: #FFFF00">eukaryotic</span>. We classify only the predominantly single-cells organisms Bacteria and Archaea as prokaryotes (pro- = “before”; -kary- = “nucleus”). Animal cells, plants, fungi, and protists are all eukaryotes (eu- = “true”)</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
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
            return redirect(url_for('training_routes.training_17', flash_message="Let's do one last task. What relationship do you think exists between these two terms?")
                        )
        else:
            return redirect(url_for('training_routes.training_16', flash_message="Everything here is correct so we can submit to finalize."))


@training_routes.route('/training_17', methods=['GET', 'POST'])
@login_required
def training_17():

    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "eukaryotic cells"
    term_2 = "protein"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>Like prokaryotes, <span style="background-color: #FFFF00">eukaryotic cells</span> have a plasma membrane, a phospholipid bilayer with embedded <span style="background-color: #FFFF00">proteins</span> that separates the internal contents of the cell from its surrounding environment.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
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
        if form.submit3.data:  # 'is inside of' is submit2 for the spatial form
            return redirect(url_for('training_routes.training_18', flash_message="Excellent job! While there definitely are connections between eukaryotic cells and proteins, here proteins refers to a component of the plasma membrane. Hence, there is no *direct* relationship.")
                        )
        else:
            return redirect(url_for('training_routes.training_17', flash_message="This isn't the right relationship for this term pair.  Let's try another one"))

@training_routes.route('/training_18', methods=['GET', 'POST'])
@login_required
def training_18():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "eukaryotic cells"
    term_2 = "protein"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>Like prokaryotes, <span style="background-color: #FFFF00">eukaryotic cells</span> have a plasma membrane, a phospholipid bilayer with embedded <span style="background-color: #FFFF00">proteins</span> that separates the internal contents of the cell from its surrounding environment.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                               next_link=url_for('training_routes.training_text_submission_1', flash_message="There is one last relationship option that we want to discuss: creating your own relationships!")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes.training_text_submission_1', flash_message="There is one last relationship option that we want tp discuss: creating your own relationships!"))


@training_routes.route('/training_text_submission_1', methods=['GET', 'POST'])
@login_required
def training_text_submission_1():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "eukaryotic cells"
    term_2 = "protein"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>Like prokaryotes, <span style="background-color: #FFFF00">eukaryotic cells</span> have a plasma membrane, a phospholipid bilayer with embedded <span style="background-color: #FFFF00">proteins</span> that separates the internal contents of the cell from its surrounding environment.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                               next_link=url_for('training_routes.training_text_submission_2', flash_message="If two terms are related, but none of the relationship buttons seem quite right, you can enter your own.")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes.training_text_submission_2', flash_message="If two terms are related, but none of the relationship buttons seem quite right, you can enter your own."))

@training_routes.route('/training_text_submission_2', methods=['GET', 'POST'])
@login_required
def training_text_submission_2():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "eukaryotic cells"
    term_2 = "protein"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>Like prokaryotes, <span style="background-color: #FFFF00">eukaryotic cells</span> have a plasma membrane, a phospholipid bilayer with embedded <span style="background-color: #FFFF00">proteins</span> that separates the internal contents of the cell from its surrounding environment.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                               next_link=url_for('training_routes.training_text_submission_3',
                                                 flash_message="Try clicking on the 'Define new relationship button'")
                               )


    if request.method == 'POST':
        # There is only one submit button so no need to check beyond "POST"

        return redirect(url_for('training_routes.training_text_submission_3', flash_message="Try clicking on the 'Define new relationship button'"))

@training_routes.route('/training_text_submission_3', methods=['GET', 'POST'])
@login_required
def training_text_submission_3():
    flash_message = request.args["flash_message"]
    form = EntityEntityForm(request.form)
    term_1 = "eukaryotic cells"
    term_2 = "protein"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>Like prokaryotes, <span style="background-color: #FFFF00">eukaryotic cells</span> have a plasma membrane, a phospholipid bilayer with embedded <span style="background-color: #FFFF00">proteins</span> that separates the internal contents of the cell from its surrounding environment.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                return redirect(url_for('training_routes.training_text_submission_4',
                                        flash_message="Now you have a text box on the right. Type in some text and click 'Submit'")
                                )
            else:
                return redirect(url_for('training_routes.training_text_submission_3',
                                        flash_message="Click on the 'Define a new relationship' button to move on"))

@training_routes.route('/training_text_submission_4', methods=['GET', 'POST'])
@login_required
def training_text_submission_4():
    flash_message = request.args["flash_message"]
    form = TextInputForm(request.form)
    term_1 = "eukaryotic cells"
    term_2 = "protein"
    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = '<h3>Like prokaryotes, <span style="background-color: #FFFF00">eukaryotic cells</span> have a plasma membrane, a phospholipid bilayer with embedded <span style="background-color: #FFFF00">proteins</span> that separates the internal contents of the cell from its surrounding environment.</h3>'
    content = Markup(content)
    content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"

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
                return redirect(url_for('training_routes.training_19'))
            else:
                return redirect(url_for('training_routes.training_text_submission_4',
                                        flash_message="Type some text and click on the 'Submit' button to move on"))

@training_routes.route('/training_19', methods=['GET', 'POST'])
@login_required
def training_19():

    # The user has finished the training, so mark training as complete
    user = db.session.query(User).filter(User.user_id == session['user_id']).first()
    user.training_complete = True
    db.session.commit()


    form = InstructionForm(request.form)
    header = "You have finished the training modules!"
    content_items = Markup(
        """
        <p>You will now be moved on to create your own relationships on new content. <br><br>
        You will spend 25 minutes on these tasks.  There is a timer in the upper right hand corner to show you how
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

        return redirect(url_for('wrst_routes.get_new_task')
                        )

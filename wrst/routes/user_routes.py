from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session
from wrst.database import db
from wrst.database.models import User
from wrst.forms.user_forms import UserLogin, UserCreation, UserEdit

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['GET', 'POST'])
def splash_page():
    # Check if the user is currently logged in via a session variable. If so, route to task. Else, to login
    if session.get('email_address', None):
        return redirect(url_for('wrst_routes.do_wrst_family'))
    else:
        return redirect(url_for('user_routes.login'))

@user_routes.route('/login_by_email', methods=['GET', 'POST'])
def login_by_email():

    # Get the users email address and check if already registered
    # If everything checks out, route to task
    # Otherwise route to user creation page

    form = UserLogin(request.form)
    if not form.validate_on_submit():
        return render_template('user_form.html',
                               main_message = "Welcome to the WRST activity ever!",
                               secondary_message = "Enter your email address to log in.  If you haven't created an account you will be redirected.",
                               form=form)

    if request.method == 'POST':
        session['study'] = "N/A"
        email_address = form.email_address.data
        user = db.session.query(User).filter(User.email == email_address).first()
        if user:
            # Set the session variable and go to the task
            session['email_address'] = email_address
            return redirect(url_for('wrst_routes.get_new_task'))
        else:
            # Need to create the user so redirect there
            return redirect(url_for('user_routes.create_user'))

@user_routes.route('/login_seed', methods=['GET', 'POST'])
def login_seed():

    # Get the users email address and check if already registered
    # If everything checks out, route to task
    # Otherwise route to user creation page

    form = UserLogin(request.form)
    if not form.validate_on_submit():
        return render_template('user_form.html',
                               main_message = "Welcome to the WRST activity ever!",
                               secondary_message = "Enter your email address to log in.  If you haven't created an account you will be redirected.",
                               form=form)

    if request.method == 'POST':
        session['study'] = 'seed data'
        session['required_time_on_task'] = 5*60 # TODO make dynamic
        email_address = form.email_address.data
        user = db.session.query(User).filter(User.email == email_address).first()
        if user:
            # Set the session variable and go to the task
            session['email_address'] = email_address
            return redirect(url_for('wrst_routes.get_new_task'))
        else:
            # Need to create the user so redirect there
            print("In login seed")
            print(session.keys())
            return redirect(url_for('user_routes.create_user'))

@user_routes.route('/login_ed', methods=['GET', 'POST'])
def login_ed():

    # Get the users email address and check if already registered
    # If everything checks out, route to task
    # Otherwise route to user creation page

    form = UserLogin(request.form)
    if not form.validate_on_submit():
        return render_template('user_form.html',
                               main_message = "Welcome to the WRST activity ever!",
                               secondary_message = "Enter your email address to log in.  If you haven't created an account you will be redirected.",
                               form=form)

    if request.method == 'POST':
        session['study'] = 'education'
        session['required_time_on_task'] = 60*5
        email_address = form.email_address.data
        user = db.session.query(User).filter(User.email == email_address).first()
        if user:
            # Set the session variable and go to the task
            session['email_address'] = email_address
            return redirect(url_for('wrst_routes.get_new_task'))
        else:
            # Need to create the user so redirect there
            return redirect(url_for('user_routes.create_user'))

@user_routes.route('/stupid', methods=['GET', 'POST'])
def stupid():
    return "stupid"


# TODO: Assign cohort based on current number of participants
@user_routes.route('/create_user', methods=['GET', 'POST'])
def create_user():

    # If we are creating/logging in a new user clear out the session
    #session.clear()

    # Get the users email address and check if already registered
    # If everything checks out, route to task
    # Otherwise route to user creation page

    if not session.get('study'):
        session['study'] = 'seed data'
    if not session.get('required_time_on_task'):
        session['required_time_on_task'] = 60*5

    form = UserCreation(request.form)
    if not form.validate_on_submit():
        return render_template('user_create.html',
                               main_message = "User creation page",
                               secondary_message = "It looks like you are new user so let's get you set up!",
                               form=form)

    if request.method == 'POST':
        print(session.keys())
        new_user = User(email=form.email_address.data,
                        contact_consent=form.agree_to_contact_field.data,
                        role=form.role_select_field.data,
                        esl=form.esl_field.data=="True",
                        english_years=form.english_years_field.data,
                        study_name=session['study'],
                        study_cohort='A',
                        required_time_on_task_seconds=session['required_time_on_task'])
        db.session.add(new_user)
        db.session.commit()

        session['email_address'] = form.email_address.data
        return redirect(url_for('instruction_routes.display_task_instructions'))

@user_routes.route('/edit_user', methods=['GET', 'POST'])
def edit_user():

    # Query the current user and get their attributes
    # Then load those attributes as defaults in the edit form
    form = UserEdit(request.form)
    current_user = db.session.query(User).filter(User.email==session['email_address']).first()
    #form.email_address.default = session['email_address']
    #form.process()  # process choices & default

    if not form.validate_on_submit():
        print("About to render")
        return render_template('user_edit.html',
                               main_message = "Edit Profile: {}".format(session['email_address']),
                               secondary_message = "Make whatever updates you want and click 'Sumbit' to finalize",
                               form=form)

    if request.method == 'POST':
        # Log whatever edits and then update the session
        print("contact_consent: ", current_user.contact_consent)
        setattr(current_user, 'contact_consent', form.agree_to_contact_field.data)
        setattr(current_user, 'role', form.role_select_field.data)
        setattr(current_user, 'esl', form.esl_field.data=="True")
        setattr(current_user, 'role', form.english_years_field.data)

        db.session.commit()

        return redirect(url_for('wrst_routes.get_new_task'))


@user_routes.route('/logout', methods=['GET', 'POST'])
def logout():

    # Remove all session variables for the user
    session.clear()

    # Reroute back to the main login page
    return redirect(url_for('user_routes.login_by_email'))



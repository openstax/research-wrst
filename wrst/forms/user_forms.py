from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Required, EqualTo

# Form ORMs
# TODO: Make tooltip texts for these!

class UserLogin(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    login_submit_button = SubmitField(label='Submit')

class UserCreation(FlaskForm):
    email_address = StringField('User ID',
                                validators=[
                                    DataRequired(),
                                    EqualTo('confirm_email', message='User ID fields must match')
                                    ]
                                )
    confirm_email = StringField('Confirm User ID')
    role_select_field = SelectField(label="Select the option that best describes you",
                                    choices=[("Intro", "I am a student currently taking introductory Biology"),
                                             ("Advanced", "I am a student taking an advanced (non-intro) Biology course"),
                                             ("Instructor", "I am a Biology instructor"),
                                             ("Other", "None of the above")
                                             ],
                                    validators=[DataRequired()]
                                    )
    esl_field = SelectField(label="Do you consider english to be your native language?",
                            choices=[("False", "Yes"),
                                     ("True", "No")
                                     ],
                            validators=[DataRequired()]
                            )
    english_years_field = SelectField(label="If you answered 'No' to the above question, how long have you spoken english?",
                                      choices=[("N/A", "N/A"),
                                               ("0-5 Years", "0-5 Years"),
                                               ("5-10 Years", "5-10 Years"),
                                               ("> 10 Years", "> 10 Years")
                                               ]
                                      )
    agree_to_contact_field = BooleanField(label="Check this box if you would be interested in us contacting you with future research oppotunities")
    create_submit_button = SubmitField(label='Submit')

class UserEdit(FlaskForm):

    role_select_field = SelectField(label="Select the option that best describes you",
                                    choices=[("Intro", "I am a student currently taking introductory Biology"),
                                             ("Advanced", "I am a student taking an advanced (non-intro) Biology course"),
                                             ("Instructor", "I am a Biology instructor"),
                                             ("Other", "None of the above")
                                             ],
                                    validators=[DataRequired()]
                                    )
    esl_field = SelectField(label="Do you consider english to be your native language?",
                            choices=[("False", "Yes"),
                                     ("True", "No")
                                     ],
                            validators=[DataRequired()]
                            )
    english_years_field = SelectField(label="If you answered 'No' to the above question, how long have you spoken english?",
                                      choices=[("N/A", "N/A"),
                                               ("0-5 Years", "0-5 Years"),
                                               ("5-10 Years", "5-10 Years"),
                                               ("> 10 Years", "> 10 Years")
                                               ]
                                      )
    agree_to_contact_field = BooleanField(label="Check this box if you would be interested in us contacting you with future research oppotunities")
    create_submit_button = SubmitField(label='Submit')

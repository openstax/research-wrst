from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, IntegerField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, Required, EqualTo

# Form ORMs
# TODO: Make tooltip texts for these!

consent_form = """
Consent Form for Participation in Research

Version: January 2019
Study Title: Convergence Accelerator Study
Principal Investigator: Dr. Richard Baraniuk
OpenStax at Rice University
6100 Main St. MS 375, Houston, TX, 77005, 713-348-5132; richb@rice.edu
Other Investigator(s): Dr. Phillip Grimaldi, Dr. Andrew Waters
_______________________________________________________________________________

You may be eligible to take part in a research study. This form gives you important information about
the study. It describes the purpose of the research, the risks and possible benefits of participating in
the study.

Purpose of this Study

The overarching goal of this research is to develop a novel method for generating knowledge graphs
(KGs). Briefly, KGs are a structured representation of knowledge in a particular domain (e.g., Physics,
Biology, etc.). KGs have many applications in educational technology, such as automatic question
generation and automated summarization. However, they are time consuming and expensive to
generate. The purpose of the study is to evaluate a new learning task designed to make generation of
these knowledge graphs easier and less expensive.
Procedures / What will happen to me in this study?
In this study, you will read an educational science text, then be asked to label the relationship
between concepts that you read about in the task. The study will take approximately 30 minutes to
complete.

Participant Requirements

In order to participate, you must be over the age of 18 and a fluent English speaker

Risks

The risks and discomfort associated with participation in this study are no greater than those
ordinarily encountered in daily life, such as reading or studying educational materials. There are no
anticipated risks from participation.
Benefits
There may be no personal benefit from your participation in the study but the knowledge received
may be of value to humanity.

Compensation & Costs

You will compensated with $10 USD for your participation. There will be no partial payment if you
cannot complete the study. There will be no cost to you if you participate in this study.
Ending the Your Participation
Your participation in this study is entirely voluntary. You are free to refuse to be in the study and your
refusal will not influence current of future relationships with Rice University and participating sites.

Confidentiality

By participating in the study, you understand and agree that Rice University may be required to disclose
your consent form, data and other personally identifiable information as required by law, regulation,
subpoena or court order. Otherwise, your confidentiality will be maintained in the following manner:
Your data and consent form will be kept separate. Your consent form will be stored in a locked location
on Rice University property and will not be disclosed to third parties. By participating, you understand
and agree that the data and information gathered during this study may be used by Rice University and
published and/or disclosed by Rice University to others outside of Rice University. However, your
name, address, contact information and other direct personal identifiers in your consent form will not
be mentioned by Rice University in any such publication or dissemination of the research data and/or
results.
The researchers will take the following steps to protect participants’ identities during this study: (1)
Each participant will be assigned a number; (2) The researchers will record any data collected during
the study by number, not by name; (3) Any original recordings or data files will be stored on secure,
encrypted servers, accessed only by authorized researchers.
Rights
Your participation is voluntary. You are free to stop your participation at any point. Refusal to
participate or withdrawal of your consent or discontinued participation in the study will not result in
any penalty or loss of benefits or rights to which you might otherwise be entitled. The Principal
Investigator may at his/her discretion remove you from the study for any of a number of reasons. In
such an event, you will not suffer any penalty or loss of benefits or rights which you might otherwise
be entitled.

Right to Ask Questions & Contact Information

If you have any questions about this study, you should feel free to ask them now.
If you have questions later regarding the study or a research-related injury, or if you have complaints,
concerns, suggestions about the research, desire additional information, or wish to withdraw your
participation please contact the Principal Investigator by mail, phone or e-mail in accordance with the
contact information listed on the first page of this consent.

For questions about your rights as a research participant, or to discuss problems, concerns or
suggestions related to the research, or to obtain information or offer input about the research, you
should contact Stephanie Thomas, Compliance Administrator, at Rice University. Email: irb@rice.edu
or Telephone: 713-348-3586

Voluntary Consent

By clicking the options below, you agree that the above information has been explained to you and all
your current questions have been answered. You understand that you may ask questions about any
aspect of this research study during the course of the study and in the future. By signing this form,
you agree to participate in this research study.

"""

class UserLogin(FlaskForm):
    email_address = StringField('Email Address', validators=[DataRequired(), Email()])
    login_submit_button = SubmitField(label='Submit')

class UserCreation(FlaskForm):
    text = TextAreaField("", default=consent_form, render_kw={"rows": 30, "cols": 7, "readonly":True})
    create_agree_button = SubmitField(label='I consent')
    create_disagree_button = SubmitField(label='I do not consent')

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

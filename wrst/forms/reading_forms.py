from flask_wtf import FlaskForm
from wtforms import SubmitField

class ReadingForm(FlaskForm):
    reading_submit_button = SubmitField(label='Next')

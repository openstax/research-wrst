from flask_wtf import FlaskForm
from wtforms import SubmitField

# Form ORMs
# TODO: Make tooltip texts for these!

class InstructionForm(FlaskForm):
    instruction_submit_button = SubmitField(label='Next screen')

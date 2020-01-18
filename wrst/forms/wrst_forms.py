from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Required, EqualTo

# Form ORMs
class FamilyForm(FlaskForm):
        type = "family"
        button_dict = {'submit0': 'Taxonomic relationship',
                       'submit1': 'Component relationship',
                       'submit2': 'Spatial relationship',
                       'submit3': 'Functional relationship',
                       'submit4': 'No direct relationship',
                       'submit5': 'I am not sure'}
        button_keys = list(button_dict.keys())
        hovertext = ["Describes subclasses or instances",
                     "Describes parts and materials that make up something",
                     "Describes where objects are located",
                     "Describes how events function on objects",
                     "Use this when there is no direct relationship between terms",
                     ""]
        submit0 = SubmitField(label=button_dict['submit0'])
        submit1 = SubmitField(label=button_dict['submit1'])
        submit2 = SubmitField(label=button_dict['submit2'])
        submit3 = SubmitField(label=button_dict['submit3'])
        submit4 = SubmitField(label=button_dict['submit4'])
        submit5 = SubmitField(label=button_dict['submit5'])


class TaxonomyForm(FlaskForm):
    type = "relationship"
    button_dict = {'submit0': 'is a type of',
                   'submit1': 'is an instance of',
                   'submit2': 'I am not sure'}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Tiger' is a type of 'cat",
                 "Ex: 'Mike is an instance of a human",
                 ""]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class ComponentForm(FlaskForm):
    type = "relationship"
    button_dict = {'submit0': 'contains',
                   'submit1': 'contains several',
                   'submit2': 'has material',
                   'submit3': 'I am not sure'}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Table' contains 'leg'",
                 "Ex: 'Mouth contains several teeth",
                 "Ex: 'Table' has material 'wood'",
                 ""]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class SpatialForm(FlaskForm):
    type = "relationship"
    button_dict = {'submit0': 'is located at',
                   'submit1': 'is outside of',
                   'submit2': 'is inside of',
                   'submit3': 'resides against',
                   'submit4': 'I am not sure'}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Cat' is at the 'box'",
                 "Ex: 'Cat' is outside the 'box'",
                 "Ex: 'Cat' is inside the 'box'",
                 "Ex: 'Cat' is against the 'box'",
                 ""]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class FunctionalForm(FlaskForm):
    type = "relationship"
    button_dict = {'submit0': 'has function',
                   'submit1': 'facilitates',
                   'submit2': 'I am not sure'}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Hammer' has function 'driving nails'",
                 "Ex: 'Hammerhead' facilitates 'nailing'",
                 ""]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class FinalSubmitForm(FlaskForm):
    type = "submit"
    submit = SubmitField(label='Looks good!')
    go_back_button = SubmitField(label='I want to redo this')

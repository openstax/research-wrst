from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Required, EqualTo

NONE_OF_THE_ABOVE_TEXT = "Define a new relationship"
NONE_OF_THE_ABOVE_HOVERTEXT = "Use this when none of the other relationships apply"

# Form ORMs
class FamilyForm(FlaskForm):
        type = "family"
        name = "basic_family"
        form_link_names = [
            'taxonomy',
            'component',
            'spatial',
            'functional',
            'no_relationship',
            'dont_know',
            'text_input'
        ]
        button_dict = {'submit0': 'Taxonomic relationship',
                       'submit1': 'Component relationship',
                       'submit2': 'Spatial relationship',
                       'submit3': 'Functional relationship',
                       'submit4': 'No direct relationship',
                       'submit5': 'I am not sure',
                       'submit6': NONE_OF_THE_ABOVE_TEXT}
        button_keys = list(button_dict.keys())
        hovertext = ["Describes subclasses or instances",
                     "Describes parts and materials that make up something",
                     "Describes where objects are located",
                     "Describes how events function on objects",
                     "Use this when there is no direct relationship between terms",
                     "Use this if you are unsure and would like to ask for another exercise",
                     NONE_OF_THE_ABOVE_HOVERTEXT]
        submit0 = SubmitField(label=button_dict['submit0'])
        submit1 = SubmitField(label=button_dict['submit1'])
        submit2 = SubmitField(label=button_dict['submit2'])
        submit3 = SubmitField(label=button_dict['submit3'])
        submit4 = SubmitField(label=button_dict['submit4'])
        submit5 = SubmitField(label=button_dict['submit5'])
        submit6 = SubmitField(label=button_dict['submit6'])


class AllFamilyForm(FlaskForm):
    type = "family"
    name = "all_family"
    form_link_names = [
        'taxonomy',
        'component',
        'spatial',
        'functional',
        'participant',
        'event_structure',
        'causal',
        'no_relationship',
        'dont_know',
        'text_input'
    ]
    button_dict = {'submit0': 'Taxonomic relationship',
                   'submit1': 'Component relationship',
                   'submit2': 'Spatial relationship',
                   'submit3': 'Functional relationship',
                   'submit4': 'Participant relationship',
                   'submit5': 'Event structure relationship',
                   'submit6': 'Causal relationship',
                   'submit7': 'No direct relationship',
                   'submit8': 'I am not sure',
                   'submit9': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Describes subclasses or instances",
                 "Describes parts and materials that make up something",
                 "Describes where objects are located",
                 "Describes how events function on objects",
                 "Use this when there is no direct relationship between terms",
                 "Describes the role of entities during events",
                 "Describes the timeline of events",
                 "Describes how events modulate other events",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    submit5 = SubmitField(label=button_dict['submit5'])
    submit6 = SubmitField(label=button_dict['submit6'])
    submit7 = SubmitField(label=button_dict['submit7'])
    submit8 = SubmitField(label=button_dict['submit8'])
    submit9 = SubmitField(label=button_dict['submit9'])


class EntityEntityForm(FlaskForm):
    type = "family"
    name = "entity_entity"
    form_link_names = [
        'taxonomy',
        'component',
        'spatial',
        'no_relationship',
        'dont_know',
        'text_input'
    ]
    button_dict = {'submit0': 'Taxonomic relationship',
                   'submit1': 'Component relationship',
                   'submit2': 'Spatial relationship',
                   'submit3': 'No direct relationship',
                   'submit4': 'I am not sure',
                   'submit5': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Describes subclasses or instances",
                 "Describes parts and materials that make up something",
                 "Describes where objects are located",
                 "Use this when there is no direct relationship between terms",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    submit5 = SubmitField(label=button_dict['submit5'])

class EntityEventForm(FlaskForm):
    type = "family"
    name = "entity_event"
    form_link_names = [
        'functional',
        'participant',
        'no_relationship',
        'dont_know',
        'text_input'
    ]

    button_dict = {'submit0': 'Functional relationship',
                   'submit1': 'Participant relationship',
                   'submit2': 'No direct relationship',
                   'submit3': 'I am not sure',
                   'submit4': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Describes how events function on object",
                 "Describes the role of entities during events",
                 "Use this when there is no direct relationship between terms",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])

class EventEventForm(FlaskForm):
    type = "family"
    name = "event_event"
    form_link_names = [
        'event_structure',
        'causal',
        'no_relationship',
        'dont_know',
        'text_input'
    ]
    button_dict = {'submit0': 'Event structure relationships',
                   'submit1': 'Causal relationship',
                   'submit2': 'No direct relationship',
                   'submit3': 'I am not sure',
                   'submit4': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Describes the timeline of events",
                 "Describes how events modulate other events",
                 "Use this when there is no direct relationship between terms",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])

class TaxonomyForm(FlaskForm):
    type = "relationship"
    name = "taxonomy"
    button_dict = {'submit0': 'is a type of',
                   'submit1': 'is an instance of',
                   'submit2': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Tiger' is a type of 'cat",
                 "Ex: 'John is a specific human",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class ComponentForm(FlaskForm):
    type = "relationship"
    name = "component"
    button_dict = {'submit0': 'contains',
                   'submit1': 'contains several',
                   'submit2': 'has material',
                   'submit3': 'I am not sure',
                   'submit4': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Table' contains 'leg'",
                 "Ex: 'Mouth contains several teeth",
                 "Ex: 'Table' has material 'wood'",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class SpatialForm(FlaskForm):
    type = "relationship"
    name = "spatial"
    button_dict = {'submit0': 'is located at',
                   #'submit1': 'is outside of',
                   'submit1': 'is inside of',
                   'submit2': 'resides against',
                   'submit3': 'I am not sure',
                   'submit4': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Cat' is at the 'box'",
                 #"Ex: 'Cat' is outside the 'box'",
                 "Ex: 'Cat' is inside the 'box'",
                 "Ex: 'Cat' is against the 'box'",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    #submit5 = SubmitField(label=button_dict['submit5'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')


class FunctionalForm(FlaskForm):
    type = "relationship_no_flip"
    name = "functional"
    button_dict = {'submit0': 'has function',
                   'submit1': 'facilitates',
                   'submit2': 'I am not sure',
                   'submit3': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: 'Hammer' has function 'driving nails'",
                 "Ex: 'Hammerhead' facilitates 'nailing'",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class EventStructureForm(FlaskForm):
    type = "relationship"
    name = "event_structure"
    button_dict = {'submit0': 'first subevent',
                   'submit1': 'subevent',
                   'submit2': 'next subevent',
                   'submit3': 'I am not sure',
                   'submit4': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: The first event of mitosis is prophase",
                 "Ex: During prophase, spindle fibers begin to form",
                 "Ex: After prophase is metaphase",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class CausalForm(FlaskForm):
    type = "relationship"
    name = "causal"
    button_dict = {'submit0': 'causes',
                   'submit1': 'enables',
                   'submit2': 'prevents',
                   'submit3': 'inhibits',
                   'submit4': 'I am not sure',
                   'submit5': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: Chemical causes reaction",
                 "Ex: Catalyst enables reaction",
                 "Ex: Lack of oxygen prevents fire ",
                 "Ex: Inhibitors inhibit reactions",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    submit5 = SubmitField(label=button_dict['submit5'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class ParticipantForm(FlaskForm):
    type = "relationship_no_flip"
    name = "participant"
    button_dict = {'submit0': 'participant',
                   'submit1': 'instrument',
                   'submit2': 'raw material',
                   'submit3': 'result',
                   'submit4': 'site',
                   'submit5': 'I am not sure',
                   'submit6': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: The virus enters a cell",
                 "Ex: The cell propels itself using a flagellum",
                 "Ex: Mitochondria uses sunlight to produce sugar",
                 "Ex: The result of mitosis are two new cells",
                 "Ex: The virus enters the cell through the cell wall",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    submit5 = SubmitField(label=button_dict['submit5'])
    submit6 = SubmitField(label=button_dict['submit6'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')

class ParticipantFormDeprecated(FlaskForm):
    type = "relationship"
    name = "participant"
    button_dict = {'submit0': 'agent',
                   'submit1': 'object',
                   'submit2': 'instrument',
                   'submit3': 'raw material',
                   'submit4': 'result',
                   'submit5': 'site',
                   'submit6': 'I am not sure',
                   'submit7': NONE_OF_THE_ABOVE_TEXT}
    button_keys = list(button_dict.keys())
    hovertext = ["Ex: Virus enters a cell",
                 "Ex: The cell is penetrated by a virus",
                 "Ex: The cell propels itself using a flagellum",
                 "Ex: Mitochondria uses sunlight to produce sugar",
                 "Ex: The result of mitosis are two new cells",
                 "Ex: The virus enters the cell through the cell wall",
                 "Use this if you are unsure and would like to ask for another exercise",
                 NONE_OF_THE_ABOVE_HOVERTEXT]
    submit0 = SubmitField(label=button_dict['submit0'])
    submit1 = SubmitField(label=button_dict['submit1'])
    submit2 = SubmitField(label=button_dict['submit2'])
    submit3 = SubmitField(label=button_dict['submit3'])
    submit4 = SubmitField(label=button_dict['submit4'])
    submit5 = SubmitField(label=button_dict['submit5'])
    submit6 = SubmitField(label=button_dict['submit6'])
    submit7 = SubmitField(label=button_dict['submit7'])
    flip_relationship = SubmitField(label='Flip Term Order')
    go_back_button = SubmitField(label='Redo Family Selection')


class FinalSubmitForm(FlaskForm):
    type = "submit"
    name = "submit"
    submit = SubmitField(label='Submit selection')
    go_back_button = SubmitField(label='I want to redo this')

class TextInputForm(FlaskForm):
    type="text_input"
    name="text_input"
    text = StringField('Relationship (30 characters or less)', validators=[Length(max=30)])
    submit = SubmitField(label='Submit response')
    go_back_button = SubmitField(label='I want to redo this')
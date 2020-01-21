# This files contains the code to deal with how to pick the next task for a given user
# TODO: Right now this is all stupid. Here is what we need to do make un-stupid
# Content exists in a database, not a local pandas frame
# We keep track of how many times tasks have been assigned and completed
# We try to keep a user within a piece of content until they have exhausted it (probably)

from flask import session, Markup, request
from wrst.database import db
from wrst.database.models import User, Relationship
from wrst.forms.wrst_forms import (
    FamilyForm,
    AllFamilyForm,
    EntityEntityForm,
    EntityEventForm,
    EventEventForm,
    TaxonomyForm,
    ComponentForm,
    SpatialForm,
    FunctionalForm,
    CausalForm,
    ParticipantForm,
    EventStructureForm,
    FinalSubmitForm
)

import pandas as pd
import numpy as np
import re

all_forms = [
    FamilyForm,
    EntityEntityForm,
    EntityEventForm,
    EventEventForm,
    TaxonomyForm,
    ComponentForm,
    SpatialForm,
    FunctionalForm,
    EventStructureForm,
    CausalForm,
    ParticipantForm
]

def get_term_list(text, all_terms):
    text_lower = text.lower()
    words = set(text_lower.split())
    term_list = list(all_terms)
    compound_terms = [t for t in term_list if ' ' in t]
    compound_terms = set(list(all_terms))

    # Extract simple single-word matches as well as full text matches
    terms_simple = (all_terms & words)
    terms_compound = set([c for c in compound_terms if c in text_lower])

    # Get all the simple terms that are substrings of the compound terms
    terms_simple_dup = set([t for t in terms_simple if any([t in t2 for t2 in terms_compound])])

    # Get the "final" term list
    final_term_list = list(terms_simple | (terms_compound - terms_simple_dup))

    # Finally, check each term to see if it a substring of any other term in the list.  If so, kill it with fire!
    occ_count = [(t1, np.sum([t1 in t2 for t2 in final_term_list])) for t1 in final_term_list]
    final_term_list = [t[0] for t in occ_count if t[1]==1]


    return final_term_list

# Pre-process all of the term and book data
df_terms = pd.read_csv('term_list.csv')
df_book = pd.read_csv('sentences_Biology_2e_parsed.csv')
df_book = df_book[df_book['chapter']==4]
df_book = df_book[df_book['section_name']=="Eukaryotic Cells"]
all_terms = set(df_terms['term'].unique().tolist())
df_book['terms'] = df_book['sentence'].apply(lambda x: get_term_list(x, all_terms))
df_book['N_terms'] = df_book['terms'].apply(lambda x: len(x))
df_book = df_book[df_book['N_terms']>=2]
df_book['sentence_id'] = list(range(0, len(df_book)))
df_book.to_csv('output.csv')

def get_text_dynamic():
    # Get a random book sentence
    sample = df_book.sample(n=1)
    text = sample['sentence'].iloc[0]
    terms = sample['terms'].iloc[0]
    content = text
    content_url = "https://archive.cnx.org/contents/{}".format(sample['page_id'].iloc[0])
    family_form_name = 'basic_family'

    # Pick two at random terms from the term set, get corresponding locations in the text
    term_selection = list(np.random.choice(terms, 2, replace=False))
    for t in term_selection:
        pattern = re.compile(t, re.IGNORECASE)
        content = pattern.sub('<span style="background-color: #FFFF00">{}</span>'.format(t), content, 1)

    sentence_id = sample['sentence_id'].iloc[0]
    term_1 = term_selection[0]
    term_2 = term_selection[1]

    # Get the types so we can select which form to use
    type_1 = df_terms[df_terms['term']==term_1].iloc[0]['type']
    type_2 = df_terms[df_terms['term'] == term_2].iloc[0]['type']
    types = [type_1, type_2]
    N_entity = sum([t=='entity' for t in types])
    N_event = sum([t=='event' for t in t])
    if N_entity == 2: # entity-entity relationship
        family_form_name = 'entity_entity'
    elif N_entity == 2: # entity-event relationship
        family_form_name = 'entity_event'
    else: # event-event relationship
        family_form_name = 'event_event'


    question_text = "What type of relationship exists between {} and {}?".format(term_1, term_2)
    content = "<h3>{}</h3>".format(content)


    # Return
    return sentence_id, term_1, term_2, family_form_name, content, question_text, content_url

def get_next_form_by_ref(form):

    # Prep the set of keys that correspond to valid form selections
    keys = list(form.button_keys)

    # Iterate over the valid form keys and return the stringified form name if there is a match
    for ii, label in enumerate(keys):
        if getattr(form, label).data:
            return form.form_link_names[ii]

    # Default behavior in case something gets messed up . . .
    return AllFamilyForm.name

def get_form_by_name(form_name):
    for form in all_forms:
        print(form_name)
        if form.name == form_name:
            return form(request.form)

    # Default form in case something gets messed up
    print("Iz bad")
    return AllFamilyForm(request.form)

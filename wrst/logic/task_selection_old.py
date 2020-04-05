# This files contains the (deprecated) code to deal with how to pick the next task for a given user
# Selection is ultimately random but tries to be smart and not deal out repeats

from flask import session, Markup, request
from wrst.database import db
from wrst.database.models import User, Relationship, Tasks
from sqlalchemy import and_, or_
from wrst.logic.experiment import Experiment
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
    FinalSubmitForm,
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
    ParticipantForm,
]

def get_term_list(text, all_terms):
    text_lower = text.lower()
    words = set(text_lower.split())
    term_list = set(all_terms)
    compound_terms = set([t for t in term_list if " " in t])

    # Extract simple single-word matches as well as full text matches
    terms_simple = all_terms & words
    terms_compound = set([c for c in compound_terms if c in text_lower])

    # Get all the simple terms that are substrings of the compound terms
    terms_simple_dup = set(
        [t for t in terms_simple if any([t in t2 for t2 in terms_compound])]
    )

    # Get the "final" term list
    final_term_list = list(terms_simple | (terms_compound - terms_simple_dup))

    # Finally, check each term to see if it a substring of any other term in the list.  If so, kill it with fire!
    occ_count = [
        (t1, np.sum([t1 in t2 for t2 in final_term_list])) for t1 in final_term_list
    ]
    final_term_list = [t[0] for t in occ_count if t[1] == 1]
    return final_term_list


def extract_rex_ch_sec(rex_link):
    pattern = "^\d{,2}\-\d{,2}"
    tmp = rex_link.split("/")[-1]
    chsec = "".join(re.findall(pattern, tmp)).split("-")
    # chsec = rex_link.split('/')[-1][0:3].split('-')
    chsec = [int(c) for c in chsec]
    return chsec


# Pre-process all of the term and book data
# Filter down the dataframe to the exact sections used in the experiments
df_terms = pd.read_csv(
    "terms_4.2_validated.csv"
    # "terms_4.2_10.1_validated_existing.csv"
)  # pd.read_csv('term_list.csv')
exp = Experiment()
readings = exp.reading_links
readings = [extract_rex_ch_sec(r) for r in readings]
dfb = pd.read_csv("sentences_Biology_2e_parsed.csv")

df_book = pd.DataFrame()
for chsec in readings:
    ch = chsec[0]
    sec = chsec[1]
    tmp = dfb[dfb["chapter"] == ch]
    tmp = tmp[tmp["section"] == sec]
    df_book = df_book.append(tmp)
# df_book = df_book[df_book['chapter']==4]
# df_book = df_book[df_book['section_name']=="Eukaryotic Cells"]
all_terms = set(df_terms["term"].unique().tolist())
df_book["terms"] = df_book["sentence"].apply(lambda x: get_term_list(x, all_terms))
df_book["N_terms"] = df_book["terms"].apply(lambda x: len(x))
df_book = df_book[df_book["N_terms"] >= 2]
df_book["sentence_id"] = list(range(0, len(df_book)))
df_book.to_csv("output.csv")

def get_text_dynamic():
    
    # Filter down to the right chapter/section for the current user
    content_url = session["reading_link"]
    chsec = extract_rex_ch_sec(content_url)
    print("Task selection")
    print(chsec)
    dfb = df_book[df_book["chapter"] == chsec[0]]
    dfb = dfb[dfb["section"] == chsec[1]]

    already_completed = True
    while already_completed:
        # Get a random book sentence
        sample = dfb.sample(n=1)
        text = sample["sentence"].iloc[0]
        terms = sample["terms"].iloc[0]
        content = text
        # content_url = "https://archive.cnx.org/contents/{}".format(sample['page_id'].iloc[0])
        # content_url = "https://openstax.org/books/biology-2e/pages/4-3-eukaryotic-cells"
        content_url = (
            "https://openstax.org/books/biology-2e/pages/4-2-prokaryotic-cells"
        )
        family_form_name = "basic_family"


        # Pick two at random terms from the term set, get corresponding locations in the text
        term_selection = list(np.random.choice(terms, 2, replace=False))
        for t in term_selection:
            pattern = re.compile(t, re.IGNORECASE)
            content = pattern.sub(
                '<span style="background-color: #FFFF00">{}</span>'.format(t),
                content,
                1,
            )

        sentence_id = sample["sentence_id"].iloc[0]

        term_1 = term_selection[0]
        term_2 = term_selection[1]

        # Get the types so we can select which form to use
        type_1 = df_terms[df_terms["term"] == term_1].iloc[0]["type"]
        type_2 = df_terms[df_terms["term"] == term_2].iloc[0]["type"]
        types = [type_1, type_2]
        N_entity = sum([t == "entity" for t in types])
        N_event = sum([t == "event" for t in t])
        if N_entity == 2:  # entity-entity relationship
            family_form_name = "entity_entity"
        elif N_entity == 2:  # entity-event relationship
            family_form_name = "entity_event"
        else:  # event-event relationship
            family_form_name = "event_event"

        question_text = "What type of relationship exists between {} and {}?".format(
            term_1, term_2
        )
        content = "<h3>{}</h3>".format(content)

        # Already did this one?
        already_completed = (
            db.session.query(Relationship.id)
            .filter(Relationship.user == session["user_id"])
            .filter(
                or_(
                    and_(Relationship.term_1 == term_1, Relationship.term_2 == term_2),
                    and_(Relationship.term_1 == term_2, Relationship.term_2 == term_1)
                )
            )
            .filter(Relationship.paragraph_id == sentence_id)
            .all()
        )

    # Return
    return (
        sentence_id,
        term_1,
        term_2,
        family_form_name,
        content,
        question_text,
        content_url,
    )


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
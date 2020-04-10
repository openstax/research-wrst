import pandas as pd
import itertools
import numpy as np
import re
import sys
sys.path.append('..')
from wrst.app import create_app
from wrst.database import db
from wrst.database.models import Tasks
from wrst.logic.experiment import Experiment

sentences_file = "../textbook_data/book/sentences_Biology_2e_parsed.csv"

def extract_rex_ch_sec(rex_link):
    pattern = "^\d{,2}\-\d{,2}"
    tmp = rex_link.split("/")[-1]
    chsec = "".join(re.findall(pattern, tmp)).split("-")
    # chsec = rex_link.split('/')[-1][0:3].split('-')
    chsec = [int(c) for c in chsec]
    return chsec

def get_term_list(text, all_terms):
    text_lower = text.lower().replace('.', '').replace(',', '').replace('-', '').replace('?', '')
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

def create_book_dataframe(sentences_file, all_terms):
    dfb = pd.read_csv(sentences_file)

    exp = Experiment()
    readings = exp.reading_links
    readings = list(dict.fromkeys(readings)) # Ensures that we drop duplicates reading links (experiment hack)
    readings = [extract_rex_ch_sec(r) for r in readings]

    # Construct the needed portion of the book from the experiment parameters
    df_book = pd.DataFrame()
    for chsec in readings:
        ch = chsec[0]
        sec = chsec[1]
        tmp = dfb[dfb["chapter"] == ch]
        tmp = tmp[tmp["section"] == sec]
        if ((ch==10) and (sec==2)): #TODO BAD HACK BRO
            tmp = tmp[tmp['sentence_id']<=122]

        df_book = df_book.append(tmp)

    # Do term extraction, etc
    df_book["terms"] = df_book["sentence"].apply(lambda x: get_term_list(x, all_terms))
    df_book["N_terms"] = df_book["terms"].apply(lambda x: len(x))
    df_book_tmp = df_book.copy()
    df_book = df_book[df_book["N_terms"] >= 2]
    df_book["sentence_id"] = list(range(0, len(df_book)))

    return df_book, df_book_tmp

def get_base_term(term, df_terms):
    # Find the term in the dataframe, return it's base pair
    term = term.lower()
    dft = df_terms[df_terms["term"]==term]
    return dft["base_term"].iloc[0]

app = create_app()
app.app_context().push()

# Read out the sentences and term files
# Weave everything together to create the task db table, which contains each possible exercise for participants

# First, purge whatever is in the Task table currently
db.session.query(Tasks).delete()
db.session.commit()

# Get the terms dataframe and the set of all terms
exp = Experiment()
readings = exp.reading_links
readings = list(dict.fromkeys(readings))  # Ensures that we drop duplicates reading links (experiment hack)
readings = [extract_rex_ch_sec(r) for r in readings]
chapter = readings[0][0]
section = readings[0][1]
terms_file = "../textbook_data/terms/processed/openstax_{}_{}.csv".format(readings[0][0], readings[0][1])
df_terms = pd.read_csv(
    terms_file
)
df_terms["term"] = df_terms["term"].apply(lambda x: x.lower())
all_terms = set(df_terms["term"].unique().tolist())
print("I have foune {} total terms".format(df_terms.shape[0]))

# Get the book dataframe, filtered down to sentences allowed in the current experiment
df_book, df_book_full = create_book_dataframe(sentences_file, all_terms)

# Now go through each sentence and assemble a task for each pairwise combination of terms found therein
task_count = 0
for ii in range(0, df_book.shape[0]):
    sentence = df_book.iloc[ii]
    terms = sentence["terms"]
    for term_combination in itertools.combinations(terms, 2):
        task = Tasks(
            task_id=task_count,
            paragraph_id=sentence["paragraph_id"],
            sentence_id=sentence["sentence_id"],
            sentence=sentence["sentence"],
            term_1=term_combination[0],
            term_2=term_combination[1],
            type_1=df_terms[df_terms["term"]==term_combination[0]].iloc[0]["type"],
            type_2=df_terms[df_terms["term"] == term_combination[1]].iloc[0]["type"],
            base_term_1=get_base_term(term_combination[0], df_terms),
            base_term_2=get_base_term(term_combination[1], df_terms)
        )
        db.session.add(task)
        task_count += 1
db.session.commit()
print("Finished doing Ch. {} Sec. {}".format(chapter, section))
print("I found {} valid sentences having at least two terms".format(df_book.shape[0]))
print("I found {} total tasks that can be completed".format(task_count))
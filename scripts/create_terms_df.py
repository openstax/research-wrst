# Take Matthew's JSON file of terms and convert to a flat dataframe
# Final structure is "term", "type", "base_term"
# where term is the form in the text, type \in {entity, event}, and base_term is lemmatized form
# Ex: cells, entity, cell

import pandas as pd
import json
import re
import os

# Make sure base directory points to the right place . . .
base_directory = '../textbook_data/terms/raw_json/'
output_directory = '../textbook_data/terms/processed/'

# Get all the files in the raw_json directory
raw_files = os.listdir(base_directory)
raw_files = [r for r in raw_files if '.json' in r]

def proc_json_file(filename):
    df_out = pd.DataFrame()

    # Open the file, convert to dict
    with open(filename) as f:
        D = json.load(f)

        keys = D.keys()
        for k in keys:
            terms = D[k]['text']
            types = D[k]['type']
            base_term = [k] * len(terms)

            dft = pd.DataFrame({'term': terms, 'type': types, 'base_term': base_term})
            df_out = df_out.append(dft)

    return df_out.drop_duplicates()

# Run through each file, do the conversion, and save the result
for file in raw_files:
    new_file_name = file.replace('.json', '.csv')
    df = proc_json_file(base_directory + file)
    df.to_csv(output_directory + new_file_name, index=None)


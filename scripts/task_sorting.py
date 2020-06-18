# Resolve output relationship data with the task data
# Do this by comparing task_ids and also the actual term pairs that show up
# Make sure things make sense

import pandas as pd
import numpy as np

def make_term_tuple(term_1, term_2):
    L = [term_1, term_2]
    return tuple(sorted(L))

def make_type_tuple(term_1, term_2, df_terms):
    type_1 = df_terms[df_terms['term_1']==term_1]['type_1'].iloc[0]
    type_2 = df_terms[df_terms['term_1'] == term_2]['type_1'].iloc[0]
    if term_1 < term_2:
        return (type_1, type_2)
    else:
        return (type_2, type_1)

# Load the task and relationship data
df_relationships = pd.read_csv('~/Desktop/wrst_data/OS_Biology_4_2/relationships_42.csv')
df_tasks = pd.read_csv('~/Desktop/wrst_data/OS_Biology_4_2/tasks_42.csv')

# Make a entity/event map for all terms
df_terms = df_tasks[['term_1', 'type_1']].append(df_tasks[['term_2', 'type_2']].rename(columns={'term_2': 'term_1', 'type_2': 'type_1'})).drop_duplicates()

# Create sorted term tuples for tasks and relationships -- this will help deal with term flip irregularities
df_relationships['term_pair'] = df_relationships.apply(lambda x: make_term_tuple(x.term_1, x.term_2), axis=1)
df_relationships['type_pair'] = df_relationships.apply(lambda x: make_type_tuple(x.term_1, x.term_2, df_terms), axis=1)
df_tasks['term_pair'] = df_tasks.apply(lambda x: make_term_tuple(x.term_1, x.term_2), axis=1)
df_tasks['type_pair'] = df_tasks.apply(lambda x: make_type_tuple(x.term_1, x.term_2, df_terms), axis=1)

# Prep for matching
df_relationships = df_relationships.rename(columns={'paragraph_id': 'sentence_id', 'task_id': 'old_task_id'})

# Now do the matching . . . for each relationship find the tasks with the same term_pair
# Then choose the task id which has the closest sentence_id to sentence_id match
df_relationships['task_id_new'] = -1
df_relationships['potential_matches'] = -1
df_relationships['sentence_id_new'] = -1
num_violations = 0
for ii in range(df_relationships.shape[0]):
    print(ii)
    term_pair = df_relationships.iloc[ii]['term_pair']
    old_task_id = df_relationships.iloc[ii]['old_task_id']
    matching_term_pair = df_tasks[df_tasks['task_id']==old_task_id].term_pair.iloc[0]
    if term_pair != matching_term_pair: # Ruh roh, fix it
        num_violations += 1
        tid = old_task_id
        matching_tasks = df_tasks[df_tasks['term_pair']==term_pair]
        matching_ids = matching_tasks['task_id'].drop_duplicates().values

        # Find which of the matching_ids is closest to sid and then match up the task ids
        idx_match = np.argmin(matching_ids-tid)
        df_relationships['task_id_new'].iloc[ii] = matching_tasks.iloc[idx_match]['task_id']
        df_relationships['potential_matches'].iloc[ii] = len(matching_ids)
        df_relationships['sentence_id_new'].iloc[ii] = matching_tasks.iloc[idx_match]['sentence_id']
    else:
        df_relationships['task_id_new'].iloc[ii] = df_relationships['old_task_id'].iloc[ii]




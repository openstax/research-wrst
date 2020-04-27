# Just grab all the individual data files and stitch together

import pandas as pd
import os

FILTER_NONCOMPLETE = True
RAW_DATA_PATH = '/Users/drew/Desktop/wrst_data/raw/'
OUTPUT_DATA_PATH = '/Users/drew/Desktop/wrst_data/'


def append_files(files):
    df_out = pd.DataFrame()
    for ii, f in enumerate(files):
        print("\t{}) {}".format(ii, f))
        dft = pd.read_csv(RAW_DATA_PATH + f)
        df_out = df_out.append(dft)
    return df_out

files = os.listdir(RAW_DATA_PATH)
user_files = [f for f in files if 'user' in f]
relationship_files = [f for f in files if 'relationship' in f]

# Append all the relationship/user files together
df_relationship_final = append_files(relationship_files)
df_user_final = append_files(user_files)

if FILTER_NONCOMPLETE:
    valid_user = df_user_final[df_user_final['task_complete']=='t']['user_id'].unique()
    df_user_final = df_user_final[df_user_final['user_id'].isin(valid_user)]
    df_relationship_final = df_relationship_final[df_relationship_final['user'].isin(valid_user)]

# Finally, we need to drop duplicates where the same user does multiple task_ids (minor code bug)
df_relationship_final = df_relationship_final.drop_duplicates(['user', 'task_id'], keep='first')

# Write files to disk
df_user_final.to_csv(OUTPUT_DATA_PATH + 'user_final.csv', index=None)
df_relationship_final.to_csv(OUTPUT_DATA_PATH + 'relationship_final.csv', index=None)


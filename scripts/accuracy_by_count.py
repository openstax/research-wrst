# Load up the relationship data, compute global modes, and see how many responses are needed to arrive there
# Do multiple random trials

import pandas as pd
import numpy as np
import matplotlib.pyplot as plot
from plotnine import *

def compute_family_relationship_modes(df):
    modes = df.groupby(['task_id'])['family'].agg(lambda x: x.value_counts().index[0]).reset_index()
    modes = modes.rename(columns={'family': 'family_mode'})
    df['relationship'] = df['relationship'].fillna('none')
    relationships_mode = df.groupby('task_id')['relationship'].agg(lambda x: x.value_counts().index[0]).reset_index()
    relationships_mode = relationships_mode.rename(columns={'relationship': 'relationship_mode'})
    modes = modes.merge(relationships_mode, how='left')
    return modes

# Params:
T = 20 # Number of trials to run per number of users sampled

# Load the data and pre-process
output_file_name = 'Biology_42_mcmc_task_output.csv'
df = pd.read_csv('~/Desktop/wrst_data/OS_Biology_4_2/relationships_42_processed.csv')
df_users = pd.read_csv('~/Desktop/wrst_data/OS_Biology_4_2/users_42.csv')
df_users = df_users[df_users['task_complete']=='t']
df_tasks = pd.read_csv('~/Desktop/wrst_data/OS_Biology_4_2/tasks_42.csv')
df = df[df['user'].isin(df_users['user_id'].unique())]
df = df.drop_duplicates(['user', 'task_id'])
df = df[df['family']!='dont_know']
df = df.dropna(subset=['family'])

# Get the minimum number of responses for a given task -- this is our upper bound
min_resp = df.groupby(['task_id'])['user'].count().min()
num_users_vector = np.round(np.linspace(2, min_resp, 10)).astype(int)

# Compute the family/relationship modes
modes_full = compute_family_relationship_modes(df)

df_results = pd.DataFrame()
for nu in num_users_vector:
    print(f"Nu {nu}")
    for nn in range(1, T):
        dft = df.groupby(['task_id']).apply(lambda x: x.sample(n=nu)).reset_index(drop=True)

        # Get the modes on the limited data
        modes_temp = compute_family_relationship_modes(dft)
        modes_temp = modes_temp.rename(columns={
            'family_mode': 'family_mode_temp',
            'relationship_mode': 'relationship_mode_temp'
        }
        )
        modes_merge = modes_full.merge(modes_temp)

        # Compute mode errors
        family_acc = (modes_merge['family_mode'] == modes_merge['family_mode_temp']).mean()
        rel_acc = (modes_merge['relationship_mode'] == modes_merge['relationship_mode_temp']).mean()

        # Store in results
        tmp_results = pd.DataFrame({
            'N': [nu],
            'T': [nn],
            'family_acc': [family_acc],
            'relationship_acc': [rel_acc]
        }
        )
        df_results = df_results.append(tmp_results)

df_results.to_csv('tmp_accuracy_results.csv')

results_agg = df_results.groupby('N')[['family_acc', 'relationship_acc']].agg(['mean', 'std'])
results_agg.columns = [' '.join(col).strip() for col in results_agg.columns.values]
results_agg = results_agg.reset_index()
results_agg = pd.melt(results_agg, id_vars=['N'])
results_agg['metric'] = results_agg['variable'].apply(lambda x: x.split(' ')[1])
results_agg['variable'] = results_agg['variable'].apply(lambda x: x.split(' ')[0])


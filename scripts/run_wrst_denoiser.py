from denoiser_new import WRSTDenoiser
import numpy as np
import pandas as pd
from scipy.stats import mode

# User parameters
input_file_name = '~/Desktop/wrst_data/OS_Biology_4_2_pedagogical/bio_42_pedogogical_final.csv'
output_file_name = '~/Desktop/wrst_data/OS_Biology_4_2_pedagogical/bio_42_mcmc_output.csv'

# Load the data
df = pd.read_csv(input_file_name)

# Old stuff for Psych data -- we did all our pre-processing beforehand for pedagogical so not necessary
#df_users = pd.read_csv('~/Desktop/wrst_data/Psych/kg_users_export_2020-08-13.csv')
#df_users = df_users[df_users['task_complete']=='t']
#df_users = df_users[df_users['user_id'].apply(lambda x: x[0]=='5')]
# df_tasks = pd.read_csv('~/Desktop/wrst_data/Psych/psych_tasks.csv', encoding='latin')
#df = df[df['user'].isin(df_users['user_id'].unique())]

df = df.drop_duplicates(['user', 'task_id'])

# Process the relationship data to remove idk and manual stuff -- then pivot into the right data format for MCMC
# This format is a numpy array of size num participants x num tasks with values in 0....K (K is num relationships)
df = df[~df['family'].isna()]
df = df[~df['family'].isin(['dont_know'])]
unique_relationships = df['family'].unique().tolist()
relationship_map = dict(zip(unique_relationships, range(0, len(unique_relationships))))
relationship_inv_map = {relationship_map[k]: k for k in relationship_map.keys()}
df['family_idx'] = df['family'].map(relationship_map)
L_df = df.pivot(index='user', columns='task_id', values='family_idx')
L = L_df.values

# Generate synthetic data
denoiser = WRSTDenoiser()

# Run .fit() and extract posterior means (mode for C)
denoiser.fit(L)
theta_hat = np.mean(denoiser.theta_mcmc, axis=1, keepdims=True)
mu_hat = np.mean(denoiser.mu_mcmc, axis=1, keepdims=True)
gamma_hat = np.mean(denoiser.gamma_mcmc, axis=1, keepdims=True)
C_hat = mode(denoiser.C_mcmc, axis=1)[0]
C_hat.shape = len(C_hat)

# Get mapping dataframes for the tasks
df_tasks_out = pd.DataFrame(
    {
        'task_id': df['task_id'].sort_values().unique().tolist(),
        'family_idx_out': C_hat,
        'difficulty': mu_hat[:, 0]
    }
)
df_tasks_out['family_out'] = df_tasks_out['family_idx_out'].map(relationship_inv_map)

# Compute family modes and fuse output mode
modes_family = df.groupby(['task_id'])['family'].agg(lambda x: x.value_counts().index[0]).reset_index()
modes_family = modes_family.rename(columns={'family': 'family_mode'})
dft = df.merge(modes_family, how='left')
modes_family = modes_family.merge(df_tasks_out, how='left')
modes_family = modes_family.drop(columns='family_idx_out')

# Compute relationship modes and fuse
# We only want the relationships who family matches the family mode
dft = dft[dft['family']==dft['family_mode']]
dft['relationship'] = dft['relationship'].fillna('NA')
modes_relationship = dft.groupby(['task_id'])['relationship'].agg(lambda x: x.value_counts().index[0]).reset_index()
modes_relationship = modes_relationship.rename(columns={'relationship': 'relationship_mode'})

# Merge it all
modes = modes_family.merge(modes_relationship, how='left')

# Finally assemble modes df with tasks to also get sentence and term pair
# df_tasks = df_tasks[['task_id', 'sentence', 'term_1', 'term_2']]
# modes = modes.merge(df_tasks, how='left')
# modes = modes[['task_id', 'sentence', 'term_1', 'term_2', 'family_mode', 'family_out', 'difficulty']]
modes.to_csv(output_file_name, index=None)
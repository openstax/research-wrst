import pandas as pd
from plotnine import *
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa

family_name_map = {
    'dont_know': 'idk',
    'event_structure': 'event',
    'causal': 'cause',
    'spatial': 'space',
    'component': 'comp',
    'taxonomy': 'tax',
    'no_relationship': 'none',
    'participant': 'part',
    'functional': 'func',
    'manual': 'man'
}

# Get the master data frame
df = pd.read_csv('/Users/drew/Desktop/wrst_data/Psych/psych_processed.csv')
df['family'] = df['family'].fillna('manual')
df['family_name_short'] = df['family'].map(family_name_map)

# Look at number of responses by task_id (do we have gaps)
task_counts = df.groupby(['task_id'])['user'].count().reset_index()
fig_task_counts = ggplot(task_counts, aes('task_id', 'user')) + geom_bar(stat='identity')

# Overall, what families are we seeing?
family_list = df['family_name_short'].value_counts().index.tolist()
family_sort_cat = pd.Categorical(df['family_name_short'], categories=family_list)
df = df.assign(family_sort_cat = family_sort_cat)
fig_family_histogram = ggplot(df, aes('family_sort_cat')) + geom_bar() +\
                       theme(axis_text_x=element_text(rotation=90, hjust=1)) +\
                       xlab('Family Category')

# Let's get an idea of homogenous family mode is by task -- skip idks for now
df_filt = df[df['family']!='dont_know']
modes = df_filt.groupby(['task_id'])['family_name_short'].agg(lambda x: x.value_counts().index[0]).reset_index()
modes = modes.rename(columns={'family_name_short': 'family_mode'})
df_filt = df_filt.merge(modes, on='task_id')
df_filt['mode_match'] = df_filt['family_name_short'] == df_filt['family_mode']
homogeneity_df = df_filt.groupby('task_id')['mode_match'].agg(['mean', 'count']).sort_values(by=['mean', 'count'])
homogeneity_df['mode_count'] = homogeneity_df['mean'] * homogeneity_df['count']
homogeneity_df['std'] = 1.96 * np.sqrt((homogeneity_df['mean']) * (1-homogeneity_df['mean']) / homogeneity_df['count'])
homogeneity_df['lower_ci'] = homogeneity_df['mean'] - homogeneity_df['std']
homogeneity_df['upper_ci'] = homogeneity_df['mean'] + homogeneity_df['std']
task_list = homogeneity_df.index.tolist()
task_list_cat = pd.Categorical(homogeneity_df.index, categories=task_list)
homogeneity_df = homogeneity_df.assign(task_list_cat = task_list_cat)
# fig_homo = ggplot(homogeneity_df, aes('task_list_cat', 'mean')) + geom_errorbar(aes(x="mn", ymin="lower_ci", ymax="upper_ci")) + coord_flip()
avg_homo = homogeneity_df['mean'].mean()
fig_homo = ggplot(homogeneity_df, aes('mean')) + geom_histogram() + xlab('Average Agreement with Task Mode')

# Repeat the homogeneity but with family:relationship

# Can we do a top 10 bottom 10 on homogeneity?
df_tmp = df_filt.groupby(['task_id', 'family_name_short'])['id'].count().reset_index()
df_pivot = df_tmp.pivot(index='task_id', columns='family_name_short', values='id').fillna(0)
df_pivot = df_pivot.merge(homogeneity_df[['task_list_cat', 'mean']], left_on='task_id', right_on='task_list_cat', how='left')
df_pivot = df_pivot.sort_values('mean', ascending=True)
# df_pivot['task_id'] = df_pivot['task_list_cat'].values.tolist()
df_cmp = df_pivot[df_pivot['mean']<1]
df_cmp = df_cmp.drop(columns=['mean'])
df_melt_bottom_5 = pd.melt(df_cmp.iloc[0:5], id_vars=['task_list_cat'])
df_melt_top_5 = pd.melt(df_cmp.iloc[-6:-1], id_vars=['task_list_cat'])

plot_bottom_5 = ggplot(df_melt_bottom_5, aes('variable', 'value')) +\
                geom_bar(stat='identity') +\
                facet_wrap('~task_list_cat') +\
                xlab('Family') +\
                ylab('Count') +\
                theme(axis_text_x=element_text(rotation=90, hjust=1))
plot_top_5 = ggplot(df_melt_top_5, aes('variable', 'value')) +\
             geom_bar(stat='identity') +\
             facet_wrap('~task_list_cat') +\
             xlab('Family') +\
             ylab('Count') +\
             theme(axis_text_x=element_text(rotation=90, hjust=1))

# Prep data to run Gwet AC1
dft=df[df["family"]!="dont_know"]
family_values = dft["family"].unique().tolist()
id_values = range(1, len(family_values)+1)
map_dict = dict(zip(family_values, id_values))
dft["family"] = dft["family"].map(map_dict)
rater_mat = dft[["task_id", "user", "family"]].pivot('task_id', 'user', 'family')
rater_mat.to_csv('~/Desktop/rater_mat.csv')

#Task table -- for merging
df_tasks = pd.read_csv('~/Desktop/wrst_data/Psych/psych_tasks.csv')

# Compute relationship mode for each task -- s.t. family is consistent with mode
df_filt = df_filt[df_filt['mode_match']]
df_filt['relationship'] = df_filt['relationship'].fillna('none')
relationships_mode = df_filt.groupby('task_id')['relationship'].agg(lambda x: x.value_counts().index[0]).reset_index()
relationships_mode = relationships_mode.rename(columns={'relationship': 'relationship_mode'})
modes = modes.merge(relationships_mode, how='left')
df_tasks = df_tasks.drop(columns='id').merge(modes)
family_inv = {family_name_map[k]: k for k in family_name_map.keys()}
df_tasks['family_mode'] = df_tasks['family_mode'].map(family_inv)
df_tasks.to_csv('~/Desktop/wrst_data/Psych/tasks_mode.csv', index=None)
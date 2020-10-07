# Run the real data through the term denoiser


# TODO: Deal with plurals! We also have a lot of compound terms that are almost matches that are just getting hacked


from term_denoiser import TermDenoiser
from rank_denoiser import RankDenoiser
import numpy as np
import pandas as pd
import string
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()

# Load the data, extract the columns of interest
df = pd.read_csv('from_scratch_2020-09-10.csv')
#df = pd.read_csv('preannotated_2020-09-10.csv')
df = df[["worker_id", "term", "object_id"]]

# Universal fit -- we don't care about object_id at all
# Simply want to get what terms are relevant globally
# Pivot the relevant worker_id, term matrix and run the MCMCt
# Get a ranking of terms and store off

# Here we do some pre-processing on the terms
# The first step deals with weird things in the current dataset that will likely get resolved, meaning that some of this won't be necessary
# The second step remove punctuation, capitalization, and lemmatizes the words to eliminate some morpohological invariants
def stupid_strip(x):
	if x.startswith('e ') or x.startswith('f ') or x.startswith('n ') or x.startswith('t ') or x.startswith('d ') or x.startswith('r '):
		return x[2:]
	else:
		return x

def lemmas(x):
	L = x.split(" ")
	return " ".join([wordnet_lemmatizer.lemmatize(x1) for x1 in L])
my_punc = string.punctuation + "“”"
df['term'] = df['term'].apply(lambda s: s.translate(s.maketrans(dict.fromkeys(my_punc))))
df['term'] = df['term'].apply(lambda x: x.replace("—", " "))
df['term'] = df['term'].apply(lambda x: x.lower().strip())
df['term'] = df['term'].apply(lambda x: stupid_strip(x))
print("Lemmatizing -- this takes a bit")
df['term'] = df['term'].apply(lambda x: lemmas(x))
print("Done!")

# Count the term counts
term_counts = df.groupby(['term'])['worker_id'].nunique().reset_index().rename(columns={'worker_id': 'id_count'})

# Run through each object_id -- pivot to wide, fillna(0), and then remelt
# Append everything together and then re-pivot
# This will ensure that we distinguish missing labels (nan) when a reviewer never saw the object_id
# and 0 where they DID see it and did not label it
df_data = pd.DataFrame()
for object_id in df['object_id'].unique():
    # Pre-munge the data
    dft = df[df['object_id']==object_id]
    dft = dft.drop_duplicates(['worker_id', 'term'])
    dft = dft.assign(dummy=1)
    df_pivot = dft.pivot(index='term', columns='worker_id', values='dummy').fillna(0)
    df_pivot['term'] = df_pivot.index.values
    df_melt = pd.melt(df_pivot, id_vars=['term'], var_name='worker_id', value_name='label')
    df_data = df_data.append(df_melt)

# Now re-pivot
df_data = df_data.sort_values(by=['worker_id', 'term', 'label']).drop_duplicates(subset=['worker_id', 'term'])
df_pivot = df_data.pivot(index='term', columns='worker_id', values='label')

# Run the Bayesian denoiser jointly on all object ids
print("Starting the Bayesian Term Denoiser")
td = TermDenoiser()
terms = df_pivot.index.tolist()
workers = df_pivot.columns.tolist()
values = df_pivot.values
td.fit(values)

# Now run the Rank Denoiser, which will count how many times a given term was selected, regardless of the reviewer
rd = RankDenoiser()
rd.fit(values)

# Let's get averages, confidence intervals, and approx rankings for each term from the Bayesian denoiser
# We also grab the rankings from the rank denoiser
term_means = np.mean(td.t_mcmc, axis=1)
term_devs = np.std(td.t_mcmc, axis=1)
lower_ci = term_means - 1.96 * term_devs
upper_ci = term_means + 1.96 * term_devs
rank_values = rd.observations_per_term

# Store off the results
df_final = pd.DataFrame({'term': terms, 'td_mean': term_means, 'td_lower_ci': lower_ci, 'td_upper_ci': upper_ci, 'observation_count': rank_values})
df_final = df_final.sort_values(by='td_mean', ascending=False)
df_final.to_csv('~/Desktop/term_denoise/denoiser_results.csv', index=None)



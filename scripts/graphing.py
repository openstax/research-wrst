import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import write_dot
import pandas as pd

# Load the output data
df = pd.read_csv('~/Desktop/tasks_mode.csv')
df = df[df['relationship_mode']!='none']
df = df.iloc[0:10]
terms = df['base_term_1'].append(df['base_term_2']).unique()

with open('grid1.dot', 'w') as f:
    f.write('digraph  G {\n')
    for ii in range(df.shape[0]):
        b1 = df.iloc[ii].base_term_1
        b2 = df.iloc[ii].base_term_2
        label = df.iloc[ii].relationship_mode
        f.write('"{}"->"{}" [xlabel="{}", len=2];\n'.format(b1, b2, label))
    f.write('}')
    f.close()

G = nx.Graph()

for t in terms:
    G.add_node(t)

# for ii in range(len(df)):
#     G.add_edge()
G.add_edge(1,2, labels=='fuckballs')
G.add_edge(1,3)
G.add_edge(3, "billy")
nx.draw(G, with_labels=True)
plt.show()

write_dot(G, "grid.dot")

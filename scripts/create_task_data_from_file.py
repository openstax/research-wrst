import pandas as pd
import sys
sys.path.append('..')
from wrst.app import create_app
from wrst.database import db
from wrst.database.models import Tasks
import os

sentences_file = "../textbook_data/bio_42/bio_42_quiz_tasks.csv"
num_repititions = 2

print(os.listdir(".."))

# Read the data
df = pd.read_csv(sentences_file)

# Purge the current db
app = create_app()
app.app_context().push()
db.session.query(Tasks).delete()
db.session.commit()


# Now go through each sentence and assemble a task for each pairwise combination of terms found therein
task_count = 0
task_list = []
for nn in range(num_repititions):
    for ii in range(0, df.shape[0]):
        row = df.iloc[ii]
        task = Tasks(
            task_id=task_count,
            paragraph_id=row["paragraph_id"],
            sentence_id=row["sentence_id"],
            sentence=row["sentence"],
            term_1=row['term_1'],
            term_2=row['term_2'],
            type_1=row['type_1'],
            type_2=row['type_2'],
            base_term_1=row['base_term_1'],
            base_term_2=row['base_term_2'],
        )
        task_list.append(task)
        task_count += 1

db.session.bulk_save_objects(task_list)
db.session.commit()
print(f"Finished the database push from the file {sentences_file}")
print(f"I uploaded {task_count} total tasks")
print(f"I did {num_repititions} repititions. There were {df.shape[0]} unique tasks")

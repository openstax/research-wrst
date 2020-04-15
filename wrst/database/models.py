from wrst.database import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(120), primary_key=True)
    training_complete = db.Column(db.Boolean)
    study_name = db.Column(db.String(120))
    study_cohort = db.Column(db.String(120))
    required_reading_time_seconds = db.Column(db.Integer)
    required_time_on_task_seconds = db.Column(db.Integer)
    task_complete = db.Column(db.Boolean)
    user_creation_time = db.Column(db.DateTime)

    def __init__(
        self,
        user_id,
        study_name,
        study_cohort,
        required_time_on_task_seconds,
        required_reading_time_seconds,
        user_creation_time=None
    ):

        self.user_id = user_id
        self.training_complete = False
        self.study_name = study_name
        self.study_cohort = study_cohort
        self.required_time_on_task_seconds = required_time_on_task_seconds
        self.required_reading_time_seconds = required_reading_time_seconds
        self.task_complete = False
        self.user_creation_time = user_creation_time

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Relationship(db.Model):
    __tablename__ = 'relationships'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    paragraph_id = db.Column(db.Integer)
    term_1 = db.Column(db.String(64))
    term_2 = db.Column(db.String(64))
    base_term_1 = db.Column(db.String(64))
    base_term_2 = db.Column(db.String(64))
    family = db.Column(db.String(120))
    relationship = db.Column(db.String(120))
    family_id_time = db.Column(db.Numeric)
    relationship_id_time = db.Column(db.Numeric)
    total_time = db.Column(db.Numeric)
    task_id = db.Column(db.Integer)
    task_completion_time = db.Column(db.DateTime)

    def __init__(
        self,
        user,
        paragraph_id,
        term_1,
        term_2,
        base_term_1,
        base_term_2,
        family,
        relationship,
        family_id_time,
        relationship_id_time,
        total_time,
        task_id=0,
        task_completion_time=None
    ):
        self.user = user
        self.paragraph_id = paragraph_id
        self.term_1 = term_1
        self.term_2 = term_2
        self.base_term_1 = base_term_1
        self.base_term_2 = base_term_2
        self.family = family
        self.relationship = relationship
        self.family_id_time = family_id_time
        self.relationship_id_time = relationship_id_time
        self.total_time = total_time
        self.task_id=task_id
        self.task_completion_time = task_completion_time

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer)
    paragraph_id = db.Column(db.Integer)
    sentence_id = db.Column(db.Integer)
    sentence = db.Column(db.String(1024))
    term_1 = db.Column(db.String(64))
    term_2 = db.Column(db.String(64))
    type_1 = db.Column(db.String(64))
    type_2 = db.Column(db.String(64))
    base_term_1 = db.Column(db.String(64))
    base_term_2 = db.Column(db.String(64))

    def __init__(
        self,
        task_id,
        paragraph_id,
        sentence_id,
        sentence,
        term_1,
        term_2,
        type_1,
        type_2,
        base_term_1=None,
        base_term_2=None
    ):
        # self.user = user
        self.task_id = task_id
        self.paragraph_id = paragraph_id
        self.sentence_id = sentence_id
        self.sentence = sentence
        self.term_1 = term_1
        self.term_2 = term_2
        self.type_1 = type_1
        self.type_2 = type_2
        self.base_term_1 = base_term_1
        self.base_term_2 = base_term_2

    def __repr__(self):
        return '<task_id {}>'.format(self.task_id)

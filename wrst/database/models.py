from wrst.database import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(120), primary_key=True)
    contact_consent = db.Column(db.Boolean)
    training_complete = db.Column(db.Boolean)
    role = db.Column(db.String(64))
    esl = db.Column(db.Boolean)
    english_years = db.Column(db.String(20))
    study_name = db.Column(db.String(120))
    study_cohort = db.Column(db.String(120))
    required_time_on_task_seconds = db.Column(db.Integer)
    task_complete = db.Column(db.Boolean)

    def __init__(
        self,
        email,
        contact_consent,
        role,
        esl,
        english_years,
        study_name,
        study_cohort,
        required_time_on_task_seconds
    ):

        self.email = email
        self.contact_consent = contact_consent
        self.training_complete = False
        self.role = role
        self.esl = esl
        self.english_years = english_years
        self.study_name = study_name
        self.study_cohort = study_cohort
        self.required_time_on_task_seconds = required_time_on_task_seconds
        self.task_complete = False

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Relationship(db.Model):
    __tablename__ = 'relationships'

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120))
    paragraph_id = db.Column(db.Integer)
    term_1 = db.Column(db.String(64))
    term_2 = db.Column(db.String(64))
    family = db.Column(db.String(120))
    relationship = db.Column(db.String(120))
    family_id_time = db.Column(db.Numeric)
    relationship_id_time = db.Column(db.Numeric)
    total_time = db.Column(db.Numeric)

    def __init__(
        self,
        user,
        paragraph_id,
        term_1,
        term_2,
        family,
        relationship,
        family_id_time,
        relationship_id_time,
        total_time
    ):
        self.user = user
        self.paragraph_id = paragraph_id
        self.term_1 = term_1
        self.term_2 = term_2
        self.family = family
        self.relationship = relationship
        self.family_id_time = family_id_time
        self.relationship_id_time = relationship_id_time
        self.total_time = total_time

    def __repr__(self):
        return '<id {}>'.format(self.id)

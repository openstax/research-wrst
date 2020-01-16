from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
    from wrst.database.models import User, Relationship
    db.drop_all()
    db.create_all()
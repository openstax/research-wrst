from flask_sqlalchemy import SQLAlchemy

import numpy
from psycopg2.extensions import register_adapter, AsIs


register_adapter(numpy.int64, AsIs)
register_adapter(numpy.float64, AsIs)

db = SQLAlchemy()


def reset_database():
    from wrst.database.models import User, Relationship
    db.drop_all()
    db.create_all()

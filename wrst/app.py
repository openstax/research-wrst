import logging.config

import os
from flask import Flask, Blueprint, session
from flask_session import Session
import redis
from wrst import settings
from wrst.routes.wrst_routes import wrst_routes
from wrst.routes.instruction_routes import instruction_routes
from wrst.routes.reading_routes import reading_routes
from wrst.routes.training_routes import training_routes
from wrst.routes.reading_training_routes import reading_training_routes
from wrst.routes.nonrelational_retrieval_training import retrieval_training_routes
from wrst.routes.training_routes_psych import training_routes_psych
from wrst.routes.user_routes import user_routes
from wrst.routes.admin_routes import admin_routes
from wrst.routes.distractor_routes import distractor_routes
from wrst.database import db, reset_database
from flask_bootstrap import Bootstrap

def configure_app(flask_app):
    flask_app.config.from_object(os.environ['APP_SETTINGS']) #SESSION_TYPE 'redis' set here
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SESSION_REDIS'] = redis.from_url(os.environ['REDIS_URL'])

def initialize_app(flask_app):
    configure_app(flask_app)
    Bootstrap(flask_app)
    Session(flask_app)
    flask_app.register_blueprint(wrst_routes)
    flask_app.register_blueprint(instruction_routes)
    flask_app.register_blueprint(reading_routes)
    flask_app.register_blueprint(training_routes)
    flask_app.register_blueprint(training_routes_psych)
    flask_app.register_blueprint(user_routes)
    flask_app.register_blueprint(admin_routes)
    flask_app.register_blueprint(distractor_routes)
    flask_app.register_blueprint(reading_training_routes)
    flask_app.register_blueprint(retrieval_training_routes)
    db.init_app(flask_app)
    db.create_all(app=flask_app)

def create_app():
    app = Flask(__name__)
    initialize_app(app)
    return app


def main():
    app = create_app()
    app.run()

if __name__ == "__main__":
    main()
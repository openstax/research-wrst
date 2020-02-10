from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session, Response, make_response
from wrst.database import db
from wrst.database.models import User, Relationship
from wrst.logic.decorators import login_required
import pandas as pd

admin_routes = Blueprint('admin_routes', __name__)

@admin_routes.route('/download_database', methods=['GET', 'POST'])
@login_required
def download_database():
    query = db.session.query(Relationship)
    df = pd.read_sql(query.statement, query.session.bind)
    resp = make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp

from flask import Blueprint, render_template, abort, flash, request, Markup, redirect, url_for, request, session, Response, make_response
from wrst.database import db
from wrst.database.models import User, Relationship
from wrst.logic.decorators import login_required
import pandas as pd
import time

distractor_routes = Blueprint('distractor_routes', __name__)


@distractor_routes.route('/distractor', methods=['GET'])
#@check_time()
#@check_distractor_time()
def distractor_task():
    if not session.get('distractor_seconds'):
        session['distractor_start_time'] = time.time()
        session['distractor_seconds'] = time.time()-session['distractor_start_time']
    else:
        session['distractor_seconds'] = time.time() - session['distractor_start_time']

    return render_template('distracting.html')

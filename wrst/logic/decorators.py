from flask import session
from functools import wraps
from flask import redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id') is None:
            return redirect(url_for('user_routes.login_seed'))
        return f(*args, **kwargs)
    return decorated_function

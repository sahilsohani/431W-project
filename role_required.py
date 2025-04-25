from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash("You don't have access to that page.", "danger")
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

buyer_required = role_required('buyer')
seller_required = role_required('seller')
helpdesk_required = role_required('helpdesk')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:  # or 'user_id' if you store it that way
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
import functools
import logging
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, logger, LDAP_Test

bp = Blueprint('auth', __name__, url_prefix='/')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        thedb = db.get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                thedb.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                thedb.commit()
            except thedb.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    logger.log_access('Register')
    return render_template('register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        thedb = db.get_db()
        error = None
        user = thedb.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        response = LDAP_Test.authenticate(username=username, password=password)

        if error is None and response:
            session.clear()
            #session['user_id'] = user['id']
            session['username'] = username
            return redirect(url_for('index'))

        flash(error)
    logger.log_access('Login')
    return render_template('login.html')

@bp.before_app_request
def load_logged_in_user():
    #user_id = session.get('user_id')
    username = session.get('username')
    if username is None:
        g.user = None
    else:
        g.user = username
        #g.user = db.get_db().execute(
        #    'SELECT * FROM user WHERE id = ?', (user_id,)
        #).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    load_logged_in_user()
    logger.log_access('Logout')
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
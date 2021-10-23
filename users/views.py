"""Functions for user account-based actions"""
# IMPORTS
import logging
from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from app import db
from models import User
from users.forms import RegisterForm, LoginForm
import pyotp

# CONFIG
users_blueprint = Blueprint('users', __name__, template_folder='templates')


# VIEWS
# view registration
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():

    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error
        # message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        pin_key=form.pin_key.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('register.html', form=form)


# view user login
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # create attribute logins if session attribute logins does not exist
    if not session.get('logins'):
        session['logins'] = 0
    # create an error message if login attempts is 3 or more
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()

    if form.validate_on_submit():

        session['logins'] += 1
        user = User.query.filter_by(email=form.email.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            if session['logins'] >= 3:
                flash('Number of incorrect logins exceeded.')
            elif session['logins'] == 3 - 1:
                flash('Login details incorrect. 1 login attempt remaining.')
            else:
                flash('Login details incorrect. ' + str(3 - session['logins']) + ' login attempts remaining.')
            return render_template('login.html', form=form)

        if pyotp.TOTP(user.pin_key).verify(form.pin.data):
            session['logins'] = 0
            login_user(user)
            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()

        else:
            flash("You have supplied an invalid 2FA token!", "danger")
            return render_template('login.html', form=form)

        return profile()
    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# view user profile
@users_blueprint.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.firstname)


# view user account
@users_blueprint.route('/account')
@login_required
def account():
    return render_template('account.html',
                           acc_no=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone)

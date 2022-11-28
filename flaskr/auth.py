from flask_login import login_user, login_required, logout_user, UserMixin, LoginManager
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flaskr.db import user_collection
import flaskr.db, bcrypt, sys
from flaskr.models import User

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User(name)
    user_from_db = user_collection.find_one({'username': name})

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not user.check_password(password.encode(), user_from_db.get('password')):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))


@auth.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    username  = request.form.get('name')
    password = request.form.get('password')
    # hashes and salts the password for storage in the database
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    # if this returns None the username doesn't already exist
    user = flaskr.db.check_for_user(username)
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # adds a new user to the database with the hashed and salted password
    flaskr.db.add_user(username, hashed_password)

    return redirect(url_for('auth.login'))

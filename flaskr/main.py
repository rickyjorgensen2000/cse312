try:
    from flask import Blueprint, render_template, redirect, url_for
    from flask import request
    from flask_login import login_required, current_user
    import flaskr.db as db
    import sys
except Exception as e:
    print(" Some pacakages are missing: {}".format(e))

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    users_data = db.check_for_user(current_user.username)
    return render_template('profile.html', name = current_user.username, wins = users_data.get('wins'), losses = users_data.get('loss'))

@main.route('/game')
@login_required
def game():
    return render_template('eric_html_files/screen_one.html')
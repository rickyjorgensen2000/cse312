try:
    from flask import Blueprint, render_template, redirect, url_for
    from flask import request
    from flask_login import login_required, current_user
    import flaskr.db as db
    import flaskr.globals as globals
    from flask_socketio import emit
    import flask_socketio
    import sys
except Exception as e:
    print(" Some pacakages are missing: {}".format(e))

main = Blueprint('main', __name__)

global counter
counter = 0


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    users_data = db.check_for_user(current_user.username)
    return render_template('profile.html', name=current_user.username, wins=users_data.get('wins'),
                           draws=users_data.get('draw'), losses=users_data.get('loss'))


@main.route('/game')
@login_required
def game():
    return render_template('eric_html_files/screen_one.html')


@main.route('/board')
@login_required
def board():
    return render_template('eric_html_files/screen_two.html')

@main.route('/leaderboard')
@login_required
def leaderboard():
    all_users_data_dict = db.get_leaderboard()
    rank=[]
    record=[]
    print(all_users_data_dict)

    for key in all_users_data_dict:
        rank.append(rank)
        record.append(all_users_data_dict[key])

    return render_template('leaderboard.html', win_loss_list = record)


@globals.socketsio.on('connect')
def test_connect(auth):
    global counter
    emit('my response', {'data': 'Connected'})
    if counter % 2 == 0:
        emit('state and player', {'State': 1, 'Player': 'X'})
    else:
        emit('state and player', {'State': 0, 'Player': 'O'})

    print("COUNTER: " + str(counter), file=sys.stderr)
    counter += 1
    sid = request.sid
    print("MADE IT HERE: " + sid, file=sys.stderr)

    @globals.socketsio.on('player move')
    def test_messages(msg):
        print("MADE IT HERE: " + str(msg), file=sys.stderr)
        emit('opponent move', msg, broadcast=True, include_self=False)



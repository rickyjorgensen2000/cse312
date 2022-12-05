try:
    from flask import Blueprint, render_template, redirect, url_for
    from flask import request
    from flask_login import login_required, current_user
    import flaskr.db as db
    import flaskr.globals as globals
    from flask_socketio import emit, join_room, leave_room
    import flask_socketio
    import asyncio
    import json
    import sys
    import time
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


@main.route('/waiting_room')
@login_required
def waiting_room():
    return render_template('waiting_room.html')


@main.route('/game_over')
@login_required
def game_over():
    return render_template('game_over.html')


@main.route('/board')
@login_required
def board():
    return render_template('eric_html_files/screen_two.html')


@main.route('/leaderboard')
@login_required
def leaderboard():
    all_users_data_dict = db.get_leaderboard()
    rank = []
    record = []
    print(all_users_data_dict)

    for key in all_users_data_dict:
        rank.append(rank)
        record.append(all_users_data_dict[key])

    return render_template('leaderboard.html', win_loss_list=record)


@main.route('/lobbies')
@login_required
def lobbies():
    return render_template('lobbies.html')


@globals.socketsio.on('connect')
def test_connect(auth):
    global counter
    emit('my response', {'data': 'Connected'})
    sid = request.sid
    if counter % 2 == 0:
        room = counter
        # db.delete_rooms()
        db.assign_room(current_user.username, room)
        join_room(str(room))
        emit('state and player and room', {'State': 1, 'Player': 'X', 'Room': room})
    else:
        room = counter - 1
        # db.delete_rooms()
        db.assign_room(current_user.username, room)
        join_room(str(room))
        emit('state and player and room', {'State': 0, 'Player': 'O', 'Room': room})

    counter += 1


@globals.socketsio.on('player move')
def test_messages(msg):
    room = db.get_users_room(current_user.username).get('room')
    emit('opponent move', msg, to=str(room), include_self=False)


@globals.socketsio.on('disconnected')
def disconnect():
    print("Disconnected", file=sys.stderr)
    # emit('end')

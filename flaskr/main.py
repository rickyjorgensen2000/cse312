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
    # db.delete_lobbies()
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


@main.route('/waiting_room/<waiting_room_id>')
@login_required
def waiting_room(waiting_room_id):
    # Create Lobby 
    if '/waiting_room/' + waiting_room_id not in db.get_lobbies():
        db.create_lobby('/waiting_room/' + str(waiting_room_id))
    # If the lobby already exists remove it as we don't want more than 2 people per lobby
    else:
        db.delete_lobby('/waiting_room/' + waiting_room_id)
    return render_template('waiting_room.html')


@main.route('/game_over/X')
@login_required
def game_over_x():
    return render_template('game_over.html', game_winner="X")

@main.route('/game_over/O')
@login_required
def game_over_o():
    return render_template('game_over.html', game_winner="O")


@main.route('/board/<game_id>')
@login_required
def board(game_id):
    db.assign_room(current_user.username, game_id)
    # Create Lobby 
    if '/board/' + game_id not in db.get_lobbies():
        db.create_lobby('/board/' + str(game_id))
    # If the lobby already exists remove it as we don't want more than 2 people per lobby
    else:
        db.delete_lobby('/board/' + game_id)
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
    active_lobbies = db.get_lobbies()
    return render_template('lobbies.html', created_lobbies = active_lobbies)


@globals.socketsio.on('connect')
def test_connect(auth):
    global counter
    emit('my response', {'data': 'Connected'})
    sid = request.sid
    if counter % 2 == 0:
        room = db.get_users_room(current_user.username).get('room')
        print(room, file=sys.stderr)
        print("STATE 1: ", file=sys.stderr)
        join_room(str(room))
        emit('state and player and room', {'State': 1, 'Player': 'X', 'Room': room})
    else:
        room = db.get_users_room(current_user.username).get('room')
        print(room, file=sys.stderr)
        print("STATE 0: ", file=sys.stderr)
        join_room(str(room))
        emit('state and player and room', {'State': 0, 'Player': 'O', 'Room': room})

    counter += 1


@globals.socketsio.on('player move')
def test_messages(msg):
    room = db.get_users_room(current_user.username).get('room')
    emit('opponent move', msg, to=str(room), include_self=False)


@globals.socketsio.on('win')
def player_win(msg):
    room = db.get_users_room(current_user.username).get('room')
    emit('Winner', msg, to=str(room), include_self=False)


@globals.socketsio.on('disconnected')
def disconnect():
    print("Disconnected", file=sys.stderr)
    # emit('end')

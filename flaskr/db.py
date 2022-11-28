from flask import Flask
from flask_pymongo import PyMongo
from operator import itemgetter
from flask_login import LoginManager
# Initialize mongo db with app
app = Flask(__name__)

# mongodb_client = PyMongo(app, uri='mongodb://localhost:27017/todo_db')
mongodb_client = PyMongo(app, uri='mongodb://mongo:27017/todo_db')
db = mongodb_client.db

user_collection = db['users']
leaderboard = db['leaderboard']

# add user as {'username' : username, 'wins' : '0', 'loss' : '0'}


def add_user(username, password):
    record = {'username': username, 'password': password, 'wins': 0, 'loss': 0}
    user_collection.insert_one(record)
    leaderboard.insert_one({username: 0})


def check_for_user(username):
    result = user_collection.find_one({'username': username})
    if result is not None:
        return result
    else:
        return None


# add a win or loss to the users stats


def update_player_stats(username: str, stat_to_change: str, increment: int):
    record = user_collection.find_one({'username': username})
    wins = record['wins']
    loss = record['loss']
    if stat_to_change == 'wins':
        wins += increment
    elif stat_to_change == 'loss':
        loss += increment
    new_record = {'$set': {'username': username, 'wins': wins, 'loss': loss}}
    user_collection.update_one({'username': username}, new_record)
    update_leaderboard(record['username'])
# change users score to {'username' : username, 'score' : new_score}... or insert if not there
# score will be an integer that ranks the player based on # games played and W/L ratio


def update_leaderboard(username):
    user = user_collection.find_one({'username': username})
    old_record = leaderboard.find({})
    old_score = None
    for record in old_record:
        data = record.popitem()
        if data[0] == user['username']:
            old_score = data[1]
    games_played = user['wins'] + user['loss']
    win_loss = user['wins'] - user['loss']
    new_score = 0
    if win_loss > 0:
        new_score = games_played * win_loss
    else:
        new_score = games_played * 0.5
    new_record = {'$set': {user['username']: new_score}}
    leaderboard.update_one({user['username']: old_score}, new_record)


# returns a dictionary of form {rank : [score, username]}


def get_leaderboard():
    records = leaderboard.find({})
    record_list = []
    # add all the users to a List of List to be sorted by score
    for record in records:
        item = record.popitem()
        username = item[0]
        score = item[1]
        record_list.append([score, username])
    sorted_list = sorted(record_list, key=itemgetter(0))
    return_leaderboard = {}
    rank = len(record_list)
    for user in sorted_list:
        return_leaderboard[rank] = user
        rank -= 1
    return return_leaderboard


def drop(collection):
    collection.drop()



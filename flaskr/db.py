from flask import Flask
from flask_pymongo import PyMongo
from operator import itemgetter
# Initialize mongo db with app
app = Flask(__name__)

mongodb_client = PyMongo(app, uri='mongodb://localhost:27017/todo_db')
db = mongodb_client.db

user_collection = db['users']
leaderboard = db['leaderboard']

# add user as {'username' : username, 'wins' : '0', 'loss' : '0'}


def add_user(username):
    user_collection.insert_one({'username': username, 'wins': 0, 'loss': 0})

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


# change users score to {'username' : username, 'score' : new_score}...
# score will be an integer that ranks the player based on # games played and W/L ratio


def update_leaderboard(username, new_score):
    record = leaderboard.find_one({'username': username})
    if record is not None:
        new_record = {'username': username, 'score': new_score}
        leaderboard.update_one({'username': username}, record)
        return True
    else:
        return False

# returns a dictionary of form {rank : [score, username]}


def get_leaderboard():
    records = leaderboard.find_all({})
    record_list = []
    # add all the users to a List of List to be sorted by score
    for record in records:
        record_list.append([record['score'], record['username']])
    sorted_list = sorted(record_list, key=itemgetter(0))
    return_leaderboard = {}
    rank = 1
    for user in sorted_list:
        return_leaderboard[rank] = user
        rank += 1
    return return_leaderboard


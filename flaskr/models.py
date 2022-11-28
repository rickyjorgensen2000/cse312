"""import bcrypt
from flaskr.db import *
from flask import *
from flask_login import LoginManager, UserMixin


class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password_hash, password):
        return bcrypt.checkpw(password_hash, password)

    @login.user_loader
    def load_user(username):
        u = user_collection.find_one({"Name": username})
        if not u:
            return None
        return User(username=u['Name'])"""

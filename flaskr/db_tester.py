import unittest
import db
import random


def random_blurb(base, size):
    digits = '0123456789'
    chars = '$#@~!%&*?'
    bank = digits + chars
    for i in range(0, size):
        base += bank[random.randint(0, len(bank) - 1)]

    return base


def get_dummy():
    username = random_blurb('user', 10)
    password = random_blurb('password', 10)
    return username, password


class MyTestCase(unittest.TestCase):
    user_to_password = {}

    def test_user_added(self):
        # get dummy data returned in form (username, password)
        dummy = get_dummy()
        username = dummy[0]
        password = dummy[1]
        self.user_to_password[username] = password
        # attempt to add the user to DB
        db.add_user(username, password)
        self.assertTrue(username in self.user_to_password.keys(), 'Key was not found in temp Ledger')
        # test the check_user function in the DB
        retrieval = db.check_for_user(username)
        self.assertEqual(username, retrieval['username'], 'user was not found in the database')
        self.assertEqual(password, retrieval['password'], 'Password did not match')
        # remove all dummies
        db.user_collection.drop()

    def test_stats(self):
        # create dummy users
        for i in range(0, 10):
            user = get_dummy()
            username = user[0]
            password = user[1]
            # add dummy user
            db.add_user(username, password)
            db.update_player_stats(username, 'wins', i)
            # check that players wins were updated correctly
            self.assertEqual(db.check_for_user(username)['wins'], i)
            # check that players wins were updated correctly
            db.update_player_stats(username, 'loss', i)
            self.assertEqual(db.check_for_user(username)['loss'], i)
        db.user_collection.drop()
        db.leaderboard.drop()

    def test_leaderboards(self):
        dummy_leaderboard = []
        for i in range(0, 10):
            dummy = get_dummy()
            username = dummy[0]
            password = dummy[1]
            db.add_user(username, password)
            db.update_player_stats(username, 'wins', i)
            dummy_leaderboard.append(username)
        # test if leaderboard is correct
        dummy_leaderboard.reverse()
        leaderboard = db.get_leaderboard()
        for i in range(1, len(dummy_leaderboard)):
            self.assertEqual(dummy_leaderboard[i-1], leaderboard[i][1])
        db.leaderboard.drop()
        db.user_collection.drop()


if __name__ == '__main__':
    unittest.main()

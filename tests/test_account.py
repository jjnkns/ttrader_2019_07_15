import sqlite3
import os
import unittest

#from model.orm 
from model.orm import ORM
from model.account import Account
from model.position import Position
from model.trade import Trade
from data.seed import seed
from data.schema import schema

DIR = os.path.dirname(__file__)
DBFILENAME = "_test.db"
DBPATH = os.path.join(DIR, DBFILENAME)

ORM.dbpath = DBPATH


class TestAccount(unittest.TestCase):
    def setUp(self):
        schema(DBPATH)
        seed(DBPATH)


    def tearDown(self):
        pass
        #os.remove(DBPATH)

    def test_save_and_pk_load(self):
        user = Account(username="Greg")
        user.save()
        self.assertIsInstance(user.values['pk'], int, 'save sets pk')

        pk = user.values['pk']
        same_user = Account.one_from_pk(pk)

        self.assertIsInstance(same_user, Account, "one_from_pk loads an Account object")

        self.assertEqual(same_user.values['username'], "Greg", "save creates database row")
        same_user.values['username'] = "Gregory"
        same_user.save()

        same_again = Account.one_from_pk(pk)

        self.assertEqual(same_again.values['username'], "Gregory", "save updates an existing row")

    def test_get_positions(self):
        user = Account.one_from_pk(1)
        positions = user.get_positions()
        self.assertIsInstance(positions, list, "get_positions returns a list")
        self.assertIsInstance(positions[0], Position, "get_positions should return Position objects")

    def test_get_position_for(self):
        user = Account.one_from_pk(1)
        position = user.get_position_for('TSLA')
        self.assertIsInstance(position, Position, "get_position should return a Position object")
        self.assertEqual(5, position['shares'])
    def test_get_trades(self):
        pass

    def test_get_trades_for(self):
        pass

    def test_check_password(self):
        user = Account()
        user_info = user.one_from_where_clause('WHERE username =?', username)
        hashed_pw = (user_info.values['password_hash'])
        hashed_pw = hashed_pw.encode()
        password = password.encode()
        return bycrypt.checkpw(password, hashed_pw)#returns True or False


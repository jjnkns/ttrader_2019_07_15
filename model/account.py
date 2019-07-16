import os
import sqlite3
import time
from collections import OrderedDict
from model.orm import ORM
#if you don't need an import don't include it
# from .trade import Trade
# from .position import Position
#from util import hash_password
# from . import util

#better to set the dbpath at the ORM subclass level rather than ORM itself
#do a __repr__ method in the subclass to give more detailed info

class Account(ORM):

    dir = "/Users/jenniferjenkins/horizon/ttrader_2019_07_13/data"
    #dir = os.path.dirname(__file__)
   
    dbfilename = "ttrader.db"
    dbpath = os.path.join(dir, dbfilename)
    print(dbpath)

    tablename = "accounts"
    fields = ["username", "password_hash", "balance"]

    createsql = """ """

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['username'] = kwargs.get('username')
        self.values['password_hash'] = kwargs.get('password_hash')
        #think about call util.set password
        self.values['balance'] = kwargs.get('balance')

    @classmethod
    def login(cls, username, password):
        """ login FIXME: check password hash with bcrypt not sha256"""
        return cls.select_one_where("WHERE username = ? and password_hash = ?",
                                    (username, hash_password(password)))

    def set_password(self, password):
        self.password_hash = util.(password)

    def get_positions(self):
        return Position.all_from_where_clause("WHERE account_pk =?", (self.values['pk'],))

    def get_position_for(self, ticker):
        """ return a Position object for the user. if the position does not 
        exist, return a new Position with zero shares."""
        position = Position.one_from_where_clause(
            "WHERE ticker =? AND account_pk =?", (ticker.lower(), self.values['pk']))
        if position is None:
            return Position(ticker=ticker.lower(), account_pk=self.values['pk'], shares=0)
        return position

    def get_trades(self):
        """ return all of the user's trades ordered by time. returns a list of
        Trade objects """
        return []

    def trades_for(self, ticker):
        """ return all of the user's trades for a given ticker. """
        #return []
        return Trade.many_where(
        "account_pk=? AND ticker=? ORDER BY time ASC",
        (self['pk'], ticker.lower()))
    #replace debugging print statements with proper unit tests
    #the try except blocks belong in the controller 
    def buy(self, ticker, amount):
        """ make a purchase! raise KeyError for a nonexistent stock and
        ValueError for insufficient funds. will create a new Trade and modify
        a Position and alters the user's balance. returns nothing """
        
        try:
            price = util.lookup_price(ticker)
            total = price*amount
        except KeyError:
            return None

        try:
            if self['balance'] > total:
                print('enough money')
                self['balance'] -= total
                self.save()
                t1 = Trade(account_pk=self['pk'], ticker=ticker, volume=amount, price=price)
                t1.save()
                p1 = Position(account_pk=self['pk'], ticker=ticker, shares=amount)
                p1.save()
                
            else:
                raise ValueError
        except ValueError:
            print('Insufficient Funds')
            return None
            

            

    def sell(self, ticker, amount):
        """ make a sale! raise KeyError for a non-existent Position and
        ValueError for insufficient shares. will create a new Trade object,
        modify a Position, and alter the self.balance. returns nothing."""
        pass
        try:
            print('Trying to lookup stock price!')
            price = util.lookup_price(ticker)
            total = price*amount
        except KeyError:
            print('No such ticker')
            return None

        try:
            print('Checking positions before selling')
            p1=Position(account_pk=self['pk'],ticker=ticker)
            current_value = p1.current_value()
            if p1['shares'] <= amount:
                print('enough shares')
                self['balance'] += current_value
                self.save()
                t1 = Trade(account_pk=self['pk'], ticker=ticker, volume=(-1*amount), price=price, time=10)
                t1.save()
            else:
                raise ValueError
        except ValueError:
            print('Insufficient shares')


if __name__=="__main__":
    # account = Account(username='Bessie', balance=0)
    # account.set_password('abc123')
    # account.save()
    #Account.login('Bessie', 'abc123')
    a1 = Account(username='Mikey23', password_hash='abc456', balance=25000)
    a1.save()
    a1.buy('AMZN',4)
    #a1.sell('AMZN',1)
    print(a1.trades_for('AMZN'))
    
    
    
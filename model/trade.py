
import os
from collections import OrderedDict
import time
from . import util
from .orm import ORM

#from account import Account

import sqlite3

class Trade(ORM):

    dir = "/Users/jenniferjenkins/horizon/ttrader_2019_07_13/data"
    #dir = os.path.dirname(__file__)
   
    dbfilename = "ttrader.db"
    dbpath = os.path.join(dir, dbfilename)

    tablename = "trades"

    # * a Trades table containing info on every single trade executed
    # * pk (the primary key of the trades table -- auto-incremented integer)
    # * account_pk (the primary key of the associated accounts table)
    # * ticker (ticker symbol, a string)
    # * volume (an integer)
    # * price (a float)
    # * time (a float, in Unix time)

    fields = ["account_pk", "ticker", "volume", "price", "time"]

    def __init__(self, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['account_pk'] = kwargs.get('account_pk')
        self.values['ticker'] = kwargs.get('ticker')
        self.values['volume'] = kwargs.get('volume')
        self.values['price'] =kwargs.get('price')
        self.values['time'] = kwargs.get('time', time.time())

t = Trade(account_pk=1, ticker='MSFT', volume=3, price =24.0)
t.save()

    
   



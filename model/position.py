import os
from collections import OrderedDict

from .orm import ORM
from .util import lookup_price

dir = "/Users/jenniferjenkins/horizon/ttrader_2019_07_13/data"
#dir = os.path.dirname(__file__)
   
dbfilename = "ttrader.db"
dbpath = os.path.join(dir, dbfilename)


class Position(ORM):

    tablename = 'positions'
    fields = ['account_pk', 'ticker', 'shares']


    def __init__(self, *args, **kwargs):
        self.values = OrderedDict()
        self.values['pk'] = kwargs.get('pk')
        self.values['account_pk'] = kwargs.get('account_pk')
        self.values['ticker'] = kwargs.get('ticker')
        self.values['shares'] = kwargs.get('shares')

    def current_value(self):
        """ current value of this postion at the current market rate. returns
        a float """
        try:
            price = util.lookup_price(self['ticker'])
        except:
            print('No such ticker')
            return None

        current_value = self['shares']*price
        return current_value
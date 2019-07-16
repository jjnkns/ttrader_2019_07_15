import requests
import bcrypt
######

#only use this when you are creating a NEW user
#remember to do x.encode or b'String'
#needs to be a byte string
def get_bcrypt_pw_hash(plain_text_pw):
    if isinstance('String',plain_text_pw):
       bytestring_pw = plain_text_pw.encode()
    # salt = bcrypt.gensalt()
    # salt resets every time function is run
    # print the salt here just to demonstrate where it is in the returned hash
    # print(f'salt: {salt}')
    # print(bcrypt.hashpw(plain_text_pw, salt))
    # this can and should be written one line 
    return bcrypt.hashpw(bytestring_pw, bcrypt.gensalt())

#use this for an existing user
def check_bcrypt_pw_hash(plain_text_pw, hashed_pw):
    # arguments need to be byte strings b'string'
    #check type of the input so that you don't encode a non-string
    
    bytestring_pw = plain_text_pw.encode()
    bytestring_hashed_pw = hashed_pw.encode()
    return bcrypt.checkpw(bytestring_pw, bytestring_hashed_pw)


def get_token():
    '''get API token from file'''
    try:
        with open('model/tokenfile.txt') as infile:
            token = infile.readline()
            return token
    except FileNotFoundError:
        print('API token file not found')


API_KEY = get_token()

FAKE_PRICES = {"symbol": "AAPL", "companyName": "Apple, Inc.", "calculationPrice": "close", "open": 201.85, "openTime": 1562765400280, "close": 203.23, "closeTime": 1562788800542, "high": 203.73, "low": 201.56, "latestPrice": 203.23, "latestSource": "Close", "latestTime": "July 10, 2019", "latestUpdate": 1562788800542, "latestVolume": 17876375, "iexRealtimePrice": 203.18, "iexRealtimeSize": 100, "iexLastUpdated": 1562788799615, "delayedPrice": 203.23, "delayedPriceTime": 1562788800542,
               "extendedPrice": 203.25, "extendedChange": 0.02, "extendedChangePercent": 0.0001, "extendedPriceTime": 1562791802875, "previousClose": 201.24, "change": 1.99, "changePercent": 0.00989, "iexMarketPercent": 0.032331554915356164, "iexVolume": 577971, "avgTotalVolume": 24623542, "iexBidPrice": 0, "iexBidSize": 0, "iexAskPrice": 0, "iexAskSize": 0, "marketCap": 935077488400, "peRatio": 16.95, "week52High": 233.47, "week52Low": 142, "ytdChange": 0.284206, "lastTradeTime": 1562788800542}


def lookup_price(ticker):
    global API_KEY
    try:
        # look at response status code to see if lookup was a success eg 200
        # take out print statements
        ticker = ticker.lower()
        stem = "https://cloud.iexapis.com/stable/stock/{}/quote?token="
        response = requests.get((stem.format(ticker) + API_KEY))
        price = response.json()["latestPrice"]
        if price > 0:
            return price
        else:
            raise KeyError
    except:
        raise KeyError

hashed_pw = get_bcrypt_pw_hash('abc123')
print(hashed_pw)
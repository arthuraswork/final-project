from enum import Enum 

class TokenCmdType(Enum):
    REGISTER = "register"
    LOGIN    = "login"
    BUY      = "buy"
    SELL     = "sell"
    BALANCE  = "balance"
    PORTFOLIO = "show-portfolio"
    EXIT      = "exit"
    GETRATE   = "get-rate"
    SHOWRATE   = "show-rate"
    CHANGE_PASSWORD = 'change-password'
    UPDATE_RATE = 'update-rates'
class TokenArgs(Enum):
    USERNAME = '--username'
    PASSWORD = '--password'
    CURRENCY = '--currency'
    AMOUNT   = '--amount'
    FROM     = '--from'
    TO       = '--to'
    TOP      = '--top'
    BASE     = '--base'
    

VALUTAS = {
    ('usd', 'USD', '$'): 'USD',
    ('eur', 'EUR', 'EURO', 'euro', '€'): 'EUR', 
    ('rub', 'RUB', '₽'): 'RUB',
    ('btc', 'BTC', 'bitcoin'): 'BTC',
    ('eth', 'ETH', ): 'ETH',
    ('gbr','GBR','pound'): 'GBR',
    ('sol', 'SOL'): 'SOL',
}

SALT_CHARSET = ['a','!','}','$','+','?','c','Q','>','x','G']
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
BASE_CURRENCY = 'USD'
MIN_PASSWORD_VALUE = 4
SALT_LEN = 6
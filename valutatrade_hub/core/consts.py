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
    CHANGE_PASSWORD = 'change-password'
class TokenArgs(Enum):
    USERNAME = '--username'
    PASSWORD = '--password'
    CURRENCY = '--currency'
    AMOUNT   = '--amount'
    FROM     = '--from'
    TO       = '--to'
    BASE     = '--base'
    

VALUTAS = {
    ('usd', 'USD', 'доллар', 'доллары', 'долларов', '$'): 'USD',
    ('eur', 'EUR', 'евро', '€'): 'EUR', 
    ('rub', 'RUB', 'рубль', 'рубли', 'рублей', '₽'): 'RUB',
    ('btc', 'BTC', 'биткоин', 'биткойн'): 'BTC',
    ('eth', 'ETH', 'эфир', 'эфириум'): 'ETH',
    ('gbp', 'GBP', 'фунт', 'фунты'): 'GBP',
    ('jpy', 'JPY', 'иена', 'иены', '¥'): 'JPY',
    ('cny', 'CNY', 'юань', 'юани'): 'CNY',
    ('sol', 'SOL', 'солана'): 'SOL',
    ('bnb', 'BNB', 'бинанс'): 'BNB',
    ('ada', 'ADA', 'кардано'): 'ADA'
}

SALT_CHARSET = ['a','!','}','$','+','?','c','Q','>','x','G']
DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
BASE_CURRENCY = 'USD'
MIN_PASSWORD_VALUE = 4
SALT_LEN = 6
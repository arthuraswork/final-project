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
    
class TokenArgs(Enum):
    USERNAME = '--username'
    PASSWORD = '--password'
    CURRENCY = '--currency'
    AMOUNT   = '--amount'
    FROM     = '--from'
    TO       = '--to'
    BASE     = '--base'
    
VALUTAS = ['USD','EUR','BTC','ETH','RUB']
salt_charset = ['a','!','}','$','+','?','c','Q','>','x','G']

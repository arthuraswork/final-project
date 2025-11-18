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
    HELP        = 'help'
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

HELP_COMMANDS = [
    "команды:",
    "регистрация и вход:",
    "  register --username имя --password пароль",
    "  login --username имя --password пароль", 
    "  change-password --password новый_пароль",
    "",
    "торговля:",
    "  buy --currency валюта --amount сумма",
    "  sell --currency валюта --amount сумма",
    "",
    "информация:",
    "  show-portfolio",
    "  get-rate --from валюта --to валюта",
    "  show-rate --top да/нет",
    "",
    "система:",
    "  update-rates",
    "  exit",
    "",
    "валюты: usd, eur, gbp, rub, btc, eth, sol",
    "можно писать так: usd, USD, $",
    "",
    "примеры:",
    "  login --username alice --password 1234",
    "  buy --currency btc --amount 0.1",
    "  sell --currency rub --amount 1000",
    "  get-rate --from usd --to eur"
]
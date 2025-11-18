from valutatrade_hub.core.utils import (RatesDB, PortfoliosDB, UsersDB, RatesHistoryDB)
from dataclasses import dataclass

@dataclass
class DatabaseManager:
    portfolio = PortfoliosDB()
    rates = RatesDB()
    users = UsersDB() 
    
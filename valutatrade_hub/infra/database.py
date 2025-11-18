from dataclasses import dataclass

from valutatrade_hub.core.utils import PortfoliosDB, RatesDB, UsersDB


@dataclass
class DatabaseManager:
    portfolio = PortfoliosDB()
    rates = RatesDB()
    users = UsersDB() 
    
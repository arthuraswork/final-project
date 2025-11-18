from dataclasses import dataclass

from valutatrade_hub.core.utils import PortfoliosDB, RatesDB, UsersDB


@dataclass
class DatabaseManager:
    """
    менеджер бд
    """
    portfolio = PortfoliosDB()
    rates = RatesDB()
    users = UsersDB() 
    
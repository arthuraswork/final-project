from dataclasses import dataclass
from datetime import datetime
from consts import SALT  
from utils import WalkerJSON
import hashlib

def hashing(password: str) -> str: 
    return hashlib.sha256(f'{password}{SALT}'.encode() ).hexdigest()



def register(user_name, password):
    hex_password = hashing(password)
    if not db.check_user(user_name):
        db.add_user(user_name,password)
        
@dataclass
class User:
    _user_id: int
    _user_name: str
    _hashed_password: str
    _salt: str
    _registration_date: datetime

    def get_user_info(self, query):
        user_name = query.get('--username')
        password  = query.get('--password')
        if self.verify_password(password):
            ...

    def change_password(self, new_password: str):
        ...
    
    def verify_password(self, user_name, password: str) -> bool:
        ...
        


@dataclass
class Wallet:
    currency_code: str
    _balance: float = 0.0
    
    def deposit(self, amount: float):
        ...
    def withdraw(self, amount: float):
        ...
    def get_balance(self):
        ...

    @property
    def balance(self):
        return self._balance
    

    @balance.setter
    def balance(self, value: float):
        if value < 0:
            ...
        self._balance = value
    
@dataclass
class Portfolio:
    _user_id: int
    _wallets: dict[str, Wallet]
    def add_currence(self, currence_code: str):
        ...
    
    def get_total_value(self,base_currence='USD'):
        ...
    
    def get_wallet(self,currency_code):
        ...

db = WalkerJSON()
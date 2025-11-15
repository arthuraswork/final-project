from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    _user_id: int
    _user_name: str
    _hashed_password: str
    _salt: str
    _registration_date: datetime
    
    def get_user_info(self, query):
        username = query.get('--username')
        password  = query.get('--password')
        if self.verify_password(username, password):
            ...

    def change_password(self, new_password: str):
        ...
    
    def verify_password(self, user_name, password: str) -> bool:
        ...

    def dict_transpil(self):
        return {'user_id':self._user_id, 'username': self._user_name,'hashed_password': self._hashed_password, 'salt':self._salt,'registration_date':self._registration_date}
        


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
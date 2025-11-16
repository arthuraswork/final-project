from datetime import datetime

class User:
    def __init__(self, user_id, user_name, hex_password, salt, registration_date):
        self._user_id = user_id 
        self._user_name = user_name
        self._hex_password = hex_password
        self._salt = salt
        self._registration_date = registration_date
    
    def get_user_info(self):
                return {
                    'user_id':self._user_id, 'username': self._user_name,
                    'hashed_password': self._hex_password, 
                    'salt': self._salt,'registration_date': self._registration_date
                    }
                
    def change_password(self, new_password: str):
        ...
    
    def verify_password(self, user_name, password: str) -> bool:
        ...

        
class Wallet:
    currency_code: str
    _balance: float = 0.0
    
    def __init__(self, currency_code, balance):
        self.currency_code = currency_code
        self._balance = balance
    
    def deposit(self, amount: float):
        ...
    def withdraw(self, amount: float):
        ...
    def get_balance(self):
        return f"{self.currency_code}: {self.balance}"

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value: float):
        if value > 0:
            self._balance = value
    
    
class Portfolio:
    
    def __init__(self, user_id: int, wallets: dict):
        self. _user_id: int = user_id
        self._wallets: dict[str, Wallet] = wallets
        
    def add_currence(self, currence_code: str):
        ...
    
    def get_total_value(self):
        ...
    
    def get_dicted_wallets(self) -> dict:
        return { 'user_id': self._user_id,
                'wallets': {
            key:{
                'balance': value.balance
                } for key, value in self._wallets.items()
            }
                }
    
    def get_wallets(self):
        return [wallet.get_balance() for wallet in self._wallets.values()]
    
    def get_balance(self, currency):
        return self._wallets.get(currency)
    
    def change_wallets_value(self, currency, new_value):
        if self.get_balance(currency):
            self._wallets[currency].balance = new_value
            return True
        return False
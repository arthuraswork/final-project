from dataclasses import dataclass
import json      
from decorators import handler_errors

@dataclass
class BaseDB:
    path = 'file.json'
    dir_path = './data/'
    @handler_errors
    def _load_data(self):
        with open(self.dir_path+self.path, 'r') as f:
            return json.load(f)
    @handler_errors
    def _save_data(self,data):
        with open(self.dir_path+self.path, 'w') as f:
            json.dump(data, f, indent=2)

        
@dataclass
class PortfoliosDB:
    path = 'portfolios.json'

@dataclass
class RatesDB:
    path = 'rates.json'

@dataclass
class UsersDB(BaseDB):
    path = 'users.json' 
    def add_user(self,user_name, password) -> bool:
        ...

    def check_password(self, user_name, password) -> bool:
        data = self._load_date()
    
    def get_user_info(self, user_name) -> bool:
        data = self._load_date()
        
    def check_user(self,user_name) -> bool:
        data = self._load_date()
            
@dataclass
class WalkerJSON:
    portfolios = PortfoliosDB()
    rates = RatesDB()
    users = UsersDB()   
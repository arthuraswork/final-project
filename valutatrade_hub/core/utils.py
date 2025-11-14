from dataclasses import dataclass
import json      
from .decorators import handler_errors

@dataclass
class BaseDB:
    path = 'file.json'
    dir_path = './data/'
    @handler_errors
    def _load_data(self) -> dict:
        with open(self.dir_path+self.path, 'r') as f:
            return json.load(f)
    @handler_errors
    def _save_data(self,data) -> dict:
        with open(self.dir_path+self.path, 'w') as f:
            json.dump(data, f, indent=2)

        
@dataclass
class PortfoliosDB(BaseDB):
    path = 'portfolios.json'

@dataclass
class RatesDB(BaseDB):
    path = 'rates.json'
    def get_rates(self, fromto, tofrom):
        data = self._load_data()
        rate = data.get(fromto)
        form: str = ''
        if rate:
            form = fromto
        if not rate:
            rate = data.get(tofrom)
            if rate:
                form = fromto
        if rate:
            rate['form'] = form
            return rate
        else:
            return {}

        
        

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
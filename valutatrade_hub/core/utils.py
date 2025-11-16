from dataclasses import dataclass
import json      
from .decorators import handler_errors
from .utils_funcs import hashing
@dataclass
class BaseDB:
    path = 'file.json'
    dir_path = './data/'
    @handler_errors
    def _load_data(self) -> list:
        with open(self.dir_path+self.path, 'r') as f:
            return json.load(f)
    @handler_errors
    def _save_data(self,data):
        with open(self.dir_path+self.path, 'w') as f:
            json.dump(data, f, indent=2)

        
@dataclass
class PortfoliosDB(BaseDB):
    path = 'portfolios.json'

    def get_wallet_info(self, user_id):
        data = self._load_data()
        for wallet in data:
            if wallet['user_id'] == user_id:
                return wallet
        else:
            return False
    def create_portfolio(self, user_id):
        data = self._load_data()
        data.append(
            {
            "user_id": user_id,
            "wallets": {
            "USD": {"balance": 0.00},
            "BTC": {"balance": 0.00},
            "EUR": {"balance": 0.00}
                }
            }
        )
        self._save_data(data)
        
    
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
    def add_user(self, userdata) -> bool:
        data = self._load_data()
        data.append(userdata)
        self._save_data(data)

    def check_password(self, user_name, password) -> bool:
        data = self._load_data()
        for user in data:
            if user['username'] == user_name:
                salt = user['salt']
                hashed_password = hashing(password=password,salt=salt)
                if user['hashed_password'] == hashed_password:
                    return True
                else:
                    return False
        else:
            return False
        
    def check_user(self,user_name) -> tuple[False, int]:
        data = self._load_data()
        for i,user in enumerate(data):
            if user['username'] == user_name:
                return True, i
        else:
            return False, len(data)
        
    def get_user_info(self, user_name) -> bool:
        data = self._load_data()
        for user in data:
            if  user['username'] == user_name:
                return user 
        
        
            
@dataclass
class WalkerJSON:
    portfolios = PortfoliosDB()
    rates = RatesDB()
    users = UsersDB()   
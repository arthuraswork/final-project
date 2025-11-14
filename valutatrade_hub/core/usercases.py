from dataclasses import dataclass
from valutatrade_hub.cli.interface import CLI
from .consts import SALT  
from .utils import WalkerJSON
import hashlib
@dataclass
class UserCase:
    cli = CLI()
    db = WalkerJSON()
    def user_request(self):
        request = self.cli.input()
        match request.get('cmd'):
            case 'register':
                self.on_register(request)
            case 'login':
                self.on_login(request)
            case 'buy':
                self.on_buy(request)
            case 'sell':
                self.on_sell(request)
            case 'balance':
                self.on_balance(request)
            case 'portfolio':
                self.on_portfolio(request)
            case 'exit':
                self.on_exit(request)
            case 'get-rate':
                self.on_get_rates(request)
            case _:
                ...
    def register(self, user_name, password):
        hex_password = hashing(password)
        if not self.db.check_user(user_name):
            self.db.add_user(user_name,hex_password)
        
    def on_login(self, query):
        user_name, password = query['args'].values() 
        hex_password = hashing(password)
        self.db.users.add_user(user_name=user_name, password=hex_password)

    def on_except(self, query):
        ...
    def on_sell(self, query):
        ...
    def on_logout(self, query):
        ...
    def on_portfolio(self, query):
        ...
    def on_balance(self, query):    
        ...
    def on_get_rates(self,query):
        
        fromto = query['args']['--from'] + '_' + query['args']['--to']
        tofrom = query['args']['--to'] + '_' + query['args']['--from'] 
        rate = self.db.rates.get_rates(fromto=fromto,tofrom=tofrom)
        if rate:
            print(
                rate['form'].replace('_',' -> '),
                rate['rate'],
                'reversed:',
                f"{(1 / rate['rate']):.8f}", 
                'updated at:', rate['updated_at']
            )
        else:
            print('rate not found')
    def on_exit(self):
        exit()        
        

def hashing(password: str) -> str: 
    return hashlib.sha256( f'{password}{SALT}'.encode() ).hexdigest()


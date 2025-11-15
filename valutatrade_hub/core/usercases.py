from dataclasses import dataclass
from datetime import datetime
from valutatrade_hub.cli.interface import CLI
from .models import User
from .utils import WalkerJSON
from .utils_funcs import hashing, salt_gen

@dataclass
class UserCase:
    cli = CLI()
    db = WalkerJSON()
    _is_logined: bool = False       
    def user_request(self):
        request = self.cli.input()
        match request.get('cmd'):
            case 'register':
                self.on_register(request['args'].get('--username'),request['args'].get('--password'))
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
                return {'cmd':'exception'}
    def on_register(self, user_name, password):
        hex_password, salt = hashing(password,salt_gen(),return_salt=True)
        collision, new_user_id = self.db.users.check_user(user_name)
        if not collision:
            user = User(
                new_user_id,
                user_name,
                hex_password,
                salt,
                datetime.now().strftime('%Y-%m-%dT%H:%M:%S')                
                    )
            self.db.users.add_user(user.dict_transpil())
        else:
            print(f'user: {user_name} already exists, choice another name')
        
    def on_login(self, query):
        user_name, password = query['args'].values() 
        hex_password = hashing(password)
        self._is_logined = self.db.users.check_password(user_name=user_name, password=hex_password)

    def on_sell(self, query):
        print(query)
        
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
        


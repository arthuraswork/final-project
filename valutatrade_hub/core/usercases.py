from dataclasses import dataclass
from datetime import datetime
from valutatrade_hub.cli.interface import CLI
from .models import User, Portfolio, Wallet
from .utils import WalkerJSON
from .utils_funcs import hashing, salt_gen
from .consts import DATEFRMT
@dataclass
class UserCase:
    cli = CLI()
    db = WalkerJSON()
    _is_logined: bool = False   
    user: User | None = None    
    portfolio: Portfolio | None = None
    def user_request(self):
        request = self.cli.input()
        match request.get('cmd'):
            case 'register':
                self.on_register(request['args'].get('--username'),request['args'].get('--password'))
            case 'login':
                self.on_login(request)
            case 'buy'|'sell'|'balance'|'show-portfolio':
                self.check_is_logined(request)
            case 'exit':
                self.on_exit(request)
            case 'get-rate':
                self.on_get_rates(request)
            
    def on_register(self, user_name, password):
        hex_password, salt = hashing(password,salt_gen(),return_salt=True)
        collision, new_user_id = self.db.users.check_user(user_name)
        if not collision:
            user = User(
                user_id=new_user_id,
                user_name=user_name,
                hex_password=hex_password,
                salt=salt,
                registration_date=datetime.now().strftime()                
                    )
            self.db.users.add_user(user.get_user_info(DATEFRMT))
            self.db.portfolios.create_portfolio(new_user_id)
        else:
            print(f'user: {user_name} already exists, choice another name')
        
    def on_login(self, query):
        user_name, password = query['args'].values() 
        self._is_logined = self.db.users.check_password(
            user_name=user_name, password=password
            )
        

        if self._is_logined:
            data = self.db.users.get_user_info(user_name)
            self.user = User(
                user_id=data['user_id'],
                user_name=data['username'],
                hex_password=data['hashed_password'],
                salt=data['salt'],
                registration_date=data['registration_date']              
                    )
            portfolio_data = self.db.portfolios.get_wallet_info(data['user_id'])
            wallets = {key:Wallet(key,value['balance']) for key, value in portfolio_data['wallets'].items()}
            self.portfolio = Portfolio(
                user_id= portfolio_data['user_id']
                wallets= wallets
            )
            print(f'You are logined as {user_name}')
        else:
            print(f'Username or password are uncorrect')
        
    def check_is_logined(self,request):
        if self._is_logined and self.user:
            match request['cmd']:
                case 'buy':
                    self.on_buy(request)
                case 'sell':
                    self.on_sell(request)
                case 'show-portfolio':
                    self.on_portfolio()
        else:
            print('First login with useername and password')
            
    def on_buy(self, query):
        print(query)   

    def on_sell(self, query):
        print(query)
        
    def on_portfolio(self):
        if self.portfolio:
            print(self.portfolio.get_wallets())
        
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


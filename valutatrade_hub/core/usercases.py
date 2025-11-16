from dataclasses import dataclass
from datetime import datetime
from valutatrade_hub.cli.interface import CLI
from .models import User, Portfolio, Wallet
from .utils import WalkerJSON
from .utils_funcs import hashing, salt_gen, calculations, transaction
from .consts import DATEFRMT, BASEVALUTA
from .decorators import handler_log_feedback

@dataclass
class UserCase:
    cli = CLI()
    db = WalkerJSON()
    _is_logined: bool = False   
    user: User | None = None    
    portfolio: Portfolio | None = None
    @handler_log_feedback
    def user_request(self):
        query = self.cli.input()
        match query.get('cmd'):
            case 'register':
                return self.on_register(query['args'].get('--username'),query['args'].get('--password'))
            case 'login':
                return self.on_login(query)
            case 'buy'|'sell'|'balance'|'show-portfolio':
                return self.check_is_logined(query)
            case 'exit':
                return self.on_exit(query)
            case 'get-rate':
                return self.on_get_rates(query)
        return 'unknown command, please try again'
            
    def on_register(self, user_name, password):
        if len(password) <= 4:
            return 'Password is too short, use password > 4'
        hex_password, salt = hashing(password,salt_gen(),return_salt=True)
        collision, new_user_id = self.db.users.check_user(user_name)
        if not collision:
            user = User(
                user_id=new_user_id,
                user_name=user_name,
                hex_password=hex_password,
                salt=salt,
                registration_date=datetime.now().strftime(DATEFRMT)                
                    )
            self.db.users.add_user(user.get_user_info())
            self.db.portfolios.create_portfolio(new_user_id)
            return 'Registration succesfull'
        else:
            return f'User: {user_name} already exists, choice another name'
    
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
            wallets = {key:Wallet(key, value['balance']) for key, value in list(portfolio_data['wallets'].items())}
            self.portfolio = Portfolio(
                user_id= portfolio_data['user_id'],
                wallets= wallets
            ) 
            return f'You are logined as {user_name}'
        else:
            return f'Username or password are uncorrect'
        
    def check_is_logined(self,request):
        if self._is_logined and self.user:
            match request['cmd']:
                case 'buy':
                    return self.on_buy(request)
                case 'sell':
                    return self.on_sell(request)
                case 'show-portfolio':
                    return self.on_portfolio()
        else:
            return 'First login with useername and password'
            
    def on_buy(self, query):
        currency, amount = query['args'].get('--currency'), float(query['args'].get('--amount'))
        rate = self.db.rates.get_rates(fromto=f'{BASEVALUTA}_{currency}', tofrom=f'{currency}_{BASEVALUTA}')
        price = calculations(rate['rate'],amount)
        
        old_balance = self.portfolio.get_balance(currency=currency) 
        base_balance = self.portfolio.get_balance(currency=BASEVALUTA)
        print(old_balance, base_balance)
        if base_balance.balance > price:
            if transaction(
    self.portfolio.change_wallets_value(currency=BASEVALUTA,new_value=base_balance.balance-price),
    self.portfolio.change_wallets_value(currency=currency, new_value=amount+old_balance.balance)
                            ):
                print(self.portfolio.get_dicted_wallets())
                self.commit_changes(self.portfolio.get_dicted_wallets())
                
        else:
            return f'Your balance is too low {base_balance.balance} < {price}'
            
    def commit_changes(self, new_portfolio_value):
        user_id = self.user.get_user_info()['user_id']
        old_data = self.db.portfolios.data
        data = old_data.copy()
        
        try:
            for i, portfolio in enumerate(data):
                if portfolio['user_id'] == user_id:
                    data[i] = new_portfolio_value
                    self.db.portfolios.update(data)
                    print(data)
        except:
            self.db.portfolios.update(old_data)
            return "db error"
                    
            
    def on_sell(self, query):
        print(query)
        
    def on_portfolio(self):
        if self.portfolio:
            return '\nYour portfolio:\n' + ';\n'.join(self.portfolio.get_wallets())
        return 'Portfolio not found, please call to our support'
        
    def on_get_rates(self,query):
        
        fromto = query['args']['--from'] + '_' + query['args']['--to']
        tofrom = query['args']['--to'] + '_' + query['args']['--from'] 
        rate = self.db.rates.get_rates(fromto=fromto,tofrom=tofrom)
        if rate:
            return f"""
    {rate['form'].replace('_',' -> ')} {rate['rate']}
    reversed: {(1 / rate['rate']):.8f}
    updated at: {rate['updated_at']}
    """
        else:
            return 'rate not found'
        



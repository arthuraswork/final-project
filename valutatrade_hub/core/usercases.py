from dataclasses import dataclass
from datetime import datetime

from valutatrade_hub.cli.interface import CLI
from valutatrade_hub.infra.database import DatabaseManager
from valutatrade_hub.infra.logger import log

from ..infra.consts import BASE_CURRENCY, DATE_FORMAT, MIN_PASSWORD_VALUE
from .decorators import handler_errors, handler_log_feedback
from .exceptoins import InsufficientFundsError
from .models import Portfolio, User, Wallet
from .utils_funcs import calculations, hashing, reversed_rate, salt_generator


@dataclass
class UserCase:
    """
    класс с бизнеслогикой - объединяет модели, работу с бд и обрабатывает cli
    """
    cli = CLI()
    db = DatabaseManager()
    _is_logined: bool = False   
    _session: User | None = None    
    portfolio: Portfolio | None = None
    @handler_log_feedback
    @handler_errors
    def user_request(self):
        """
        вторичная обработка запросов пользователя
        """
        query = self.cli.input()
        match query.get('cmd'):
            case 'register':
                return self.on_register(query)
            case 'login':
                return self.on_login(query)
            case 'buy'|'sell'|'balance'|'show-portfolio'|'change-password':
                return self.check_is_logined(query)
            case 'exit':
                return 'exit'
            case 'get-rate'|'show-rate':
                if query.get('cmd') == 'show-rate':
                    if query['args'].get('--top'):
                        return self.on_show_rate(query) 
                return self.on_get_rates(query)
            case 'update-rates':
                return 'update-rates'
        return 'unknown command, please try again'
    
    def on_show_rate(self, query):
        """
        выводит отсортированные валюты 
        """
        order = True if query['args']['--top'] == 'true' else False
        return self.db.rates.get_all(order)
    
    def on_change_password(self, query):
        """
        меняет пароль
        """
        new_password = query['args'].get('--password')
        if len(new_password) < MIN_PASSWORD_VALUE:
            return 'New password is too short'
        hashed_new_password, salt = hashing(
                                new_password,salt_generator(), 
                                            return_salt=True
                                            )
        if self._session.change_password(new_password=hashed_new_password, new_salt =salt):
            return self.commit_changes_user_data()

        
            
    def on_register(self, query):
        """
        регистрирует, на вход юзернейм и пароль ->
        проверка коллизий по юзернейму ->
        одобавление модели и в бд
        """
        user_name = query['args'].get('--username')
        password = query['args'].get('--password')
        if len(password) <= MIN_PASSWORD_VALUE:
            return 'Password is too short, use password > 4'
        hex_password, salt = hashing(password,salt_generator(),return_salt=True)
        collision, new_user_id = self.db.users.check_user(user_name)
        if not collision:
            user = User(
                user_id=new_user_id,
                user_name=user_name,
                hex_password=hex_password,
                salt=salt,
                registration_date=datetime.now().strftime(DATE_FORMAT)                
                    )
            self.db.users.add_user(user.get_user_info())
            self.db.portfolio.create_portfolio(new_user_id)
            return 'Registration succesfull'
        else:
            return f'User: {user_name} already exists, choice another name'
    
    def on_login(self, query):
        """
        проверяет правильность пароля пользователя
        если да, начало сессии
        """
        user_name, password = query['args'].values() 
        self._is_logined = self.db.users.check_password(
            user_name=user_name, password=password
            )
        if self._is_logined:
            data = self.db.users.get_user_info(user_name)
            self._session = User(
                user_id=data['user_id'],
                user_name=data['username'],
                hex_password=data['hashed_password'],
                salt=data['salt'],
                registration_date=data['registration_date']              
                    )
            portfolio_data = self.db.portfolio.get_wallet_info(data['user_id'])
            wallets = {
                key:Wallet(key, value['balance']) for key, value in list(
                    portfolio_data['wallets'].items()
                    )
                }
            self.portfolio = Portfolio(
                user_id= portfolio_data['user_id'],
                wallets= wallets
            ) 
            return f'You are logined as {user_name}'
        else:
            return 'Username or password are uncorrect'

    def check_is_logined(self,query):
        """
        проверка сессии для персольных запросов
        """
        if self._is_logined and self._session:
            match query['cmd']:
                case 'buy':
                    return self.on_buy(query)
                case 'sell':
                    return self.on_sell(query)
                case 'show-portfolio':
                    return self.on_portfolio()
                case 'change-password':
                    return self.on_change_password(query)
        else:
            return 'First login with useername and password'
   
    def on_buy(self, query):
        """
        логика покупки + расчеты + проверки
        на вход данные о валюте ->
        подсчет стоимости ->
        изменение в модели
        коммит или откат модели и бд
        """
        target_currency = query['args'].get('--currency')
        amount = float(query['args'].get('--amount'))
        rate = self.db.rates.currency_rate(
            fromto=f'{BASE_CURRENCY}_{target_currency}',
            tofrom=f'{target_currency}_{BASE_CURRENCY}'
            )
        price = calculations(reversed_rate(rate['rate']),amount)

        log.show(f'{target_currency}: {amount} for {price} {BASE_CURRENCY}')
        
        if self.portfolio.change_wallets_value(
                currency=BASE_CURRENCY,
                amount= price,
                operation='w'
                ):
            if self.portfolio.change_wallets_value(
                currency=target_currency, 
                amount= amount, 
                operation= 'd'
                ):
                    return self.commit_changes_portfolio(
                        self.portfolio.get_dicted_wallets()
                                                         )
        self.backup_portfolio()
        raise InsufficientFundsError()
    
    def commit_changes_user_data(self) -> str:
        """
        коммит бд с юзерами 
        """
        user_data = self._session.get_user_info()
        old_data = self.db.users.data
        data = old_data.copy()
        try:
            for i, user in enumerate(data):
                if user['username'] == user_data['username']:
                    data[i] = user_data
                    self.db.users.update(data)
                    return 'succesfull'
            return 'User not found'
        except Exception as e:
            self.db.portfolio.update(old_data)
            log.alert(f"DB error: {e}, changes not saved")

    def commit_changes_portfolio(self, new_portfolio_value):
        """
        коммит бд с портфолио
        """
        user_id = self._session.get_user_info()['user_id']
        old_data = self.db.portfolio.data
        data = old_data.copy()
        try:
            for i, portfolio in enumerate(data):
                if portfolio['user_id'] == user_id:
                    data[i] = new_portfolio_value
                    self.db.portfolio.update(data)
                    return 'succesfull'
            return 'Wallet not found'
        except Exception as e:
            self.db.portfolio.update(old_data)
            log.alert(f"DB error: {e}, changes not saved")
        
    def backup_portfolio(self):
        """
        бэкап портфолио при ошибке записи
        """
        old_data = self.db.portfolio.data
        self.db.portfolio.update(old_data)
                    

    def on_sell(self, query):
        """
        логика продажи
        """
        target_currency = query['args'].get('--currency')
        amount = float(query['args'].get('--amount'))

        rate = self.db.rates.currency_rate(
            fromto=f'{target_currency}_{BASE_CURRENCY}',
            tofrom=f'{BASE_CURRENCY}_{target_currency}'
                )['rate']
        price = calculations(rate,amount)

        log.info(f'{BASE_CURRENCY}: {price} for {target_currency} {amount} ({rate})')

        if self.portfolio.change_wallets_value(
                currency=target_currency,
                amount= amount,
                operation='w'
                ):
            if self.portfolio.change_wallets_value(
                currency=BASE_CURRENCY, 
                amount= price, 
                operation= 'd'
                ):
                    return self.commit_changes_portfolio(
                        self.portfolio.get_dicted_wallets()
                        )
        self.backup_portfolio()        
        raise InsufficientFundsError()
        
    def on_portfolio(self):
        """
        выдает инфу о портфеле + общий баланс
        """
        if self.portfolio:
            total_value = self.portfolio.get_total_value(
                self.db.rates.data,BASE_CURRENCY
                )
            log.show('\nYour portfolio:\n',
                     ';\n'.join(self.portfolio.get_wallets()),
                     f'\nTotal value: {total_value} {BASE_CURRENCY}')
            
        return 'Portfolio not found, please call to our support'
        
    def on_get_rates(self,query):
        """
        дает информацию о курсах валют
        на вход валюта 1 => валюта два
        на выход курс + обратный курс
        """
        fromto = query['args']['--from'] + '_' + query['args']['--to']
        tofrom = query['args']['--to'] + '_' + query['args']['--from'] 
        rate = self.db.rates.currency_rate(fromto=fromto,tofrom=tofrom)
        if rate:
            return f"""
    {fromto.replace('_',' -> ')} {rate['rate']}
    reversed: {reversed_rate(rate['rate'])}
    updated at: {rate['updated_at']}
    """
        else:
            return 'Rate not found'
        

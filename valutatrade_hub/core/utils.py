import json
from dataclasses import dataclass

from ..infra.decorators import handler_errors
from .utils_funcs import hashing, reversed_rate


@dataclass
class BaseDB:
    """
    базовый класс работы с бд
    """
    path = 'file.json'
    dir_path = './data/'
    
    def _load_data(self) -> list:
        """
        загрузка данных
        """
        try:    
            with open(self.dir_path+self.path, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {'exception':e}

    def _save_data(self,data):
        """
        перезапись данных
        """
        try:    
            with open(self.dir_path+self.path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            return {'exception':e}
            
    @property
    def data(self):
        """
        загрузка данных для доступа извне
        """
        return self._load_data()
    
    def update(self, data):
        """
        обновление данных дл ядоступа извне
        """
        self._save_data(data)

        
@dataclass
class PortfoliosDB(BaseDB):
    """
    реализация класса управления бд портфелей
    """
    path = 'portfolios.json'
    @handler_errors
    def get_wallet_info(self, user_id) -> list:
        """
        информация о кошельке
        """
        data = self._load_data()
        for wallet in data:
            if wallet['user_id'] == user_id:
                return wallet
        else:
            return False
    @handler_errors
    def create_portfolio(self, user_id):
        """
        создания портфеля новому юзеру
        """
        data = self._load_data()
        data.append(
            {
            "user_id": user_id,
            "wallets": {
            "USD": {"balance": 0.00}
                }
            }
        )
        self._save_data(data)

    
@dataclass
class RatesDB(BaseDB):
    path = 'rates.json'
    @handler_errors
    def currency_rate(self, fromto, tofrom):
        """
        добыча курса для валют
        если не получится ВАЛЮТА1_ВАЛЮТА2
        попробуем ВАЛЮТА2_ВАЛЮТА1
        """
        data = self._load_data()
        rate = data.get(fromto)
        form = ''
        
        if rate:
            form = fromto
        else:
            rate = data.get(tofrom)
            if rate:
                rate = rate.copy()  
                rate['rate'] = reversed_rate(rate['rate'])
                form = tofrom
        if rate:
            rate['form'] = form
            return rate
        else:
            return {}
        
    @handler_errors    
    def get_all(self, order):
        """
        загрузка всей информации о валютах
        """
        data = [(k, v) for k, v in self._load_data().items() if k[:3] == 'USD']
        sorted_data = sorted(data, key=lambda x: x[1]['rate'], reverse=order)
        return ';'.join(
            [f"\n{currency}: {info['rate']}" for currency, info in sorted_data])
        
@dataclass
class UsersDB(BaseDB):
    """
    база данных юзеров
    """
    path = 'users.json' 
    def add_user(self, userdata) -> bool:
        """
        добавление юзера в бд
        """
        data = self._load_data()
        data.append(userdata)
        self._save_data(data)
    @handler_errors
    def check_password(self, user_name, password) -> bool:
        """
        проверка пароля
        """
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
    @handler_errors
    def check_user(self,user_name) -> tuple[bool, int]:
        """
        проверка коллизии на юзернейм
        """
        data = self._load_data()
        for i,user in enumerate(data):
            if user['username'] == user_name:
                return True, i
        else:
            return False, len(data)
    @handler_errors    
    def get_user_info(self, user_name) -> bool:
        """
        информация о полбзователе
        """
        data = self._load_data()
        for user in data:
            if  user['username'] == user_name:
                return user 
            
class RatesHistoryDB(BaseDB):

    """
    база данных работы с историей курсов
    """
    path = 'exchange_rates.json'

    def update_history(self, new_rate):
        """
        перезапись
        """
        data = self._load_data()
        data.append(new_rate)
        self._save_data(data)
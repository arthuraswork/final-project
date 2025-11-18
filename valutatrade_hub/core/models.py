class User:
    """
    модель пользователя - хранит его данные
    """
    def __init__(self, user_id, user_name, hex_password, salt, registration_date):
        self._user_id = user_id 
        self._user_name = user_name
        self._hex_password = hex_password
        self._salt = salt
        self._registration_date = registration_date
    
    def get_user_info(self):
                """информаци о пользователе в виде списка"""
                return {
                    'user_id':self._user_id, 'username': self._user_name,
                    'hashed_password': self._hex_password, 
                    'salt': self._salt,'registration_date': self._registration_date
                    }
                
    def change_password(self, new_password: str, new_salt: str):
        """смена пароля"""
        self._hex_password = new_password
        self._salt  = new_salt
        return True
        
class Wallet:
    """
    модель кошелька
    """
    currency_code: str
    _balance: float = 0.0
    
    def __init__(self, currency_code, balance):
        self.currency_code = currency_code
        self._balance = balance
    
    def deposit(self, amount: float):
        """
        пополнение счета
        """
        if amount > 0:
            self._balance += amount
            return True
        return False
    def withdraw(self, amount: float):

        """
        снятие со счета
        """

        if (self._balance - amount) > 0 and amount > 0:
            self._balance -= amount
            return True
        return False
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
    """
    портфель юзера - вся информация
    о кошельках
    """
    def __init__(self, user_id: int, wallets: dict):
        self. _user_id: int = user_id
        self._wallets: dict[str, Wallet] = wallets
        
    def add_currence(self, currency: str):
        """
        добавление кошелька
        """
        self._wallets[currency] = Wallet(currency_code=currency, balance=0.00)
    
    def get_total_value(self, rates, base_currency):
        """
        сумма всех значений в базовой валюте
        """
        total = 0.0
        for wallet in self._wallets.values():
            if wallet.currency_code == base_currency:
                total += wallet.balance
            else:
                pair = f"{wallet.currency_code}_{base_currency}"
                if pair in rates:
                    total += wallet.balance * rates[pair]["rate"]
        return total
            
    def get_dicted_wallets(self) -> dict:
        """
        словарное предстваление портфеля
        """
        return { 'user_id': 
                    self._user_id,
                'wallets': {
                    key:{
                'balance': value.balance
                } for key, value in self._wallets.items()
                            }
                }
    
    def get_wallets(self):
        """
        выдача балансов кошельков
        """
        return [wallet.get_balance() for wallet in self._wallets.values()]
    
    def get_balance(self, currency):
        """
        выдача баланса конкретного кошелька
        """
        balance = self._wallets.get(currency)
        if balance:
            return balance
        self.add_currence(currency=currency)
        return self._wallets.get(currency)
        
    def change_wallets_value(self, currency, amount, operation):
        """
        смена значения в кошельке в зависимости от операции
        w == снятие d == пополнение
        """
        if self.get_balance(currency):
            if operation == 'w':
                return self._wallets[currency].withdraw(amount)
            elif operation == 'd':
                return self._wallets[currency].deposit(amount)
            return False
        raise False
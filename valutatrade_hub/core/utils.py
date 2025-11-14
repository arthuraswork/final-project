from dataclasses import dataclass
import json

@dataclass
class WalkerJSON:
    dir_path: str = './data/'
    portfolios: str = 'portfolios.json'
    rates: str = 'rates.json'
    users: str = 'users.json'            
    
    def add_user(self,user_name, password) -> bool:
        with open(self.dir_path+self.users, 'a') as f:
            ...
    
    def check_password(self, user_name, password) -> bool:
        with open(self.dir_path+self.users, 'r') as f:
            ...
    
    def get_user_info(self, user_name) -> bool:
        with open(self.dir_path+self.users, 'r') as f:
            ...
    def check_user(self,user_name) -> bool:
        with open(self.dir_path+self.users, 'r') as f:
            ...
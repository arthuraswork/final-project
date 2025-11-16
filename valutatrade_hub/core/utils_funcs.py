import hashlib
import random as rd 
from .consts import SALTCHARSET
def hashing(password: str,salt:str, return_salt = False) -> str: 
    hashed_password = hashlib.sha256( f'{password}{salt}'.encode() ).hexdigest()
    if return_salt:
        return hashed_password, salt
    return hashed_password

salt_gen = lambda: f'{rd.choice(SALTCHARSET)}'.join([
    rd.choice(SALTCHARSET) for _ in range(6)
    ])

def calculations(rate, amount):
    return rate * amount

def transaction(func1,func2):
    if func1 and func2:
        return True
    return False    
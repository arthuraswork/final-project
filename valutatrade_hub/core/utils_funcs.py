import hashlib
import random as rd 
from .consts import SALT_CHARSET, SALT_LEN

def hashing(password: str,salt:str, return_salt = False) -> str|tuple[str,str]: 
    hashed_password = hashlib.sha256( f'{password}{salt}'.encode() ).hexdigest()
    if return_salt:
        return hashed_password, salt
    return hashed_password

def salt_generator():
    charset = [rd.choice(SALT_CHARSET) for _ in range(SALT_LEN)]
    string_repr = f'{rd.choice(SALT_CHARSET)}'.join(charset)
    return string_repr
def calculations(rate, amount):
    return rate * amount

def reversed_rate(rate):
    return f"{(1 / rate):.8f}"
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

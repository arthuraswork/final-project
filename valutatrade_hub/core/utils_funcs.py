import hashlib
import random as rd

from ..infra.consts import SALT_CHARSET, SALT_LEN


def hashing(password: str,salt:str, return_salt = False) -> str|tuple[str,str]: 
    """хэширование + соление"""
    hashed_password = hashlib.sha256( f'{password}{salt}'.encode() ).hexdigest()
    if return_salt:
        return hashed_password, salt
    return hashed_password

def salt_generator():
    """генерация солей"""
    charset = [rd.choice(SALT_CHARSET) for _ in range(SALT_LEN)]
    string_repr = f'{rd.choice(SALT_CHARSET)}'.join(charset)
    return string_repr
def calculations(rate, amount) -> float:
    """расчет стоимости всего колва валют"""
    return rate * amount

def reversed_rate(rate):
    """расчет обратного курса"""

    return round(1 / rate, 8)
from dataclasses import dataclass

import requests

from .config import ParserConfig


@dataclass
class BaseAPI:
    
    config = ParserConfig()

    def request(self):
        ...

    def get(self):
        try:
            return self.request()
        except Exception as e:
            return e

@dataclass
class CoinGeckoClient(BaseAPI):
    
    def request(self):
        response = requests.get(
            f"{self.config.COINGECKO_URL}/simple/price",
            params={
                'ids': ','.join(self.config.CRYPTO_ID_MAP.values()),
                'vs_currencies': self.config.BASE_CURRENCY, 
            }
        )
        return response.json()

@dataclass
class ExchangeRateClient(BaseAPI):
    
    def request(self):
        response = requests.get(
            f"{self.config.EXCHANGERATE_API_URL}/{self.config.EXCHENGE_API_KEY}/latest/{self.config.BASE_CURRENCY}"
        )
        return response.json()
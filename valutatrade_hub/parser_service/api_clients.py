from .config import ParserConfig
from datetime import datetime
from valutatrade_hub.core.consts import DATE_FORMAT
import requests

class ParserAPI:
    
    def __init__(self):
        self.config = ParserConfig()

    def parse(self,response_coingecko, response_exchangerate):
        dt = datetime.now().strftime(DATE_FORMAT)
        coingecko_return = {f'{self.config.BASE_CURRENCY}_{self.config.REVERSED_CRYPTO_ID_MAP[k]}':{
            'rate':v, 'updated_at': dt
            } for k, v in response_coingecko.items()
              if k in self.config.CRYPTO_ID_MAP.values()}
        exchangerate_return = {
            f'{self.config.BASE_CURRENCY}_{k}':{
                "rate":v, 'updated_at':dt
                } for k, v in response_exchangerate['conversion_rates'].items()
                if k in self.config.FIAT_CURRENCIES
            } 
        return

    def get(self):
        response_coingecko = requests.get(
            f"{self.config.COINGECKO_URL}/simple/price",
                                          params={
            'ids':   ','.join(self.config.CRYPTO_ID_MAP.values()),
            'vs_currencies': self.config.BASE_CURRENCY,
            'x_cg_demo_api_key': self.config.COIN_GECKO_API_KEY  
        })
        response_exchangerate = requests.get(
        f"{self.config.EXCHANGERATE_API_URL}/{self.config.EXCHENGE_API_KEY}/latest/{self.config.BASE_CURRENCY}")
        
        return self.parse(response_coingecko=response_coingecko.json(), response_exchangerate=response_exchangerate.json())
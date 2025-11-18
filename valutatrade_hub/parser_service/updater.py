from datetime import datetime
from .config import ParserConfig
from valutatrade_hub.infra.consts import DATE_FORMAT
from .api_clients import CoinGeckoClient, ExchangeRateClient
from valutatrade_hub.infra.database import DatabaseManager  
from valutatrade_hub.core.decorators import handler_api_errors
from .storage import HistoryManager
from valutatrade_hub.infra.logger import log
class RatesUpdater:
    def __init__(self):
        self.config = ParserConfig()
        self.coingecko_api = CoinGeckoClient()
        self.exchange_api  = ExchangeRateClient() 
        self.db = DatabaseManager()
        self.historydb = HistoryManager()

    @handler_api_errors
    def update(self):
        coingecko_rate = self.coingecko_api.get()
        exchange_rate  = self.exchange_api.get()
        if coingecko_rate and exchange_rate:
            new_rates = self.parse(coingecko_rate,exchange_rate )
            log.info('Saving data ...')    
            self.save_rates(new_rates)
            log.info('Rates updated')
            return True
        log.alert('DB updating error')
        return False

    def parse(self,response_coingecko:dict, response_exchangerate:dict):
        dt = datetime.now().strftime(DATE_FORMAT)
        coingecko_return = {f'{self.config.BASE_CURRENCY}_{self.config.REVERSED_CRYPTO_ID_MAP[k]}':{
            'rate':v['usd'], 'updated_at': dt
            } for k, v in response_coingecko.items()
              if k in self.config.CRYPTO_ID_MAP.values()}
        exchangerate_return = {
            f'{self.config.BASE_CURRENCY}_{k}':{
                "rate":v, 'updated_at':dt
                } for k, v in response_exchangerate['conversion_rates'].items()
                if k in self.config.FIAT_CURRENCIES
            } 
        final_dict = coingecko_return | exchangerate_return
        final_dict['sources'] = {'crypto_rates': self.config.COINGECKO_URL, 'fiat_rates': self.config.EXCHANGERATE_API_URL}
        final_dict['timestamp'] = dt
        return final_dict

    def save_rates(self, rates):
        self.db.rates.update(rates)
        self.save_to_history(rates)

    def save_to_history(self,rates):
        self.historydb.history.update_history(rates)


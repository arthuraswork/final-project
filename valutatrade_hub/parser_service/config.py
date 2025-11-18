import os
class ParserConfig:
    
    def __init__(self):
        self.EXCHENGE_API_KEY = os.getenv('EXCHANGERATE_API_KEY')
        self.COIN_GECKO_API_KEY = os.getenv('COIN_GECKO_API_KEY') 
        self.COINGECKO_URL: str = "https://api.coingecko.com/api/v3"
        self.EXCHANGERATE_API_URL: str = "https://v6.exchangerate-api.com/v6" 
        self.BASE_CURRENCY: str = "USD"
        self.FIAT_CURRENCIES: tuple = ("EUR", "GBP", "RUB")
        self.CRYPTO_CURRENCIES: tuple = ("BTC", "ETH", "SOL")
        self.CRYPTO_ID_MAP: dict = {
            "BTC": "bitcoin", 
            "ETH": "ethereum",
            "SOL": "solana",
        }

        self.REVERSED_CRYPTO_ID_MAP = {v:k for k,v in self.CRYPTO_ID_MAP.items()}

        self.RATES_FILE_PATH: str = "data/rates.json"
        self.HISTORY_FILE_PATH: str = "data/exchange_rates.json"

        # Сетевые параметры
        self.REQUEST_TIMEOUT: int = 10
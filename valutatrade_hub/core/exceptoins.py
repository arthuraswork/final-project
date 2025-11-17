class InsufficientFundsError(Exception):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return 'Your balance is insufficient'
    
class CurrencyNotFoundError(Exception):
    def __init__(self):
        super().__init__()
    def __str__(self):
        return 'Valuta not found'
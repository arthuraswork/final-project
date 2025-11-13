from dataclasses import dataclass
from parser import ParserCLI 
import readline

def enable_arrow_keys():
    ...
def set_history_length():
    readline.set_history_length(100)

def handler_errors(func):
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            print(f'Ошибка: {e}')
    return wrapper


@dataclass
class CLI:
    parser = ParserCLI()
    prompt: str = '>>>'
    @handler_errors
    def input(self):
        user_input = input(self.prompt)
        result = self.parser.run(user_input)
        match result['cmd']:
            case 'register':
                self.on_register(result)
            case 'login':
                self.on_login(result)
            case 'buy':
                self.on_buy(result)
            case 'sell':
                self.on_sell(result)
            case 'balance':
                self.on_balance(result)
            case 'portfolio':
                self.on_portfolio(result)
            case 'logout':
                self.on_logout(result)
            case 'exit':
                self.on_exit(result)
            case 'unknown':
                self.on_unknown(result)
            case 'exception':
                self.on_except(result)
            case _:
                self.on_unknown(result)

            
        
    def on_register(self, query):
        ...
    def on_login(self, query):
        ...
    def on_unknown(self, query):
        ...
    def on_except(self, query):
        ...
    def on_sell(self, query):
        ...
    def on_logout(self, query):
        ...
    def on_portfolio(self, query):
        ...
    def on_balance(self, query):    
        ...
    def on_exit(self, query):
        exit()        
while True:
    CLI().input()
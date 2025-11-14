from dataclasses import dataclass
from parser import ParserCLI 
import readline
from valutatrade_hub.core.decorators import handler_logger

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
                if result['args'].get('--username') & result['args'].get('--password'):
                    return result
            case 'login':
                if result['args'].get('--username') & result['args'].get('--password'):
                    return result
            case 'buy':
                pass
            case 'sell':
                pass
            case 'balance':
                pass
            case 'portfolio':
                pass
            case 'exit':
                exit()
            case _:
                ...


from dataclasses import dataclass
from .parser import ParserCLI 
import readline
from valutatrade_hub.core.consts import VALUTAS
from valutatrade_hub.core.decorators import handler_logger, handler_errors

def enable_arrow_keys():
    ...
def set_history_length():
    readline.set_history_length(100)


@dataclass
class CLI:
    parser = ParserCLI()
    prompt: str = '>>>'
    @handler_errors
    def input(self) -> dict:
        user_input = input(self.prompt)
        result = self.parser.run(user_input)
        match result['cmd']:
            case 'register':
                if result['args'].get('--username') and result['args'].get('--password'):
                    return result
            case 'login':
                if result['args'].get('--username') and result['args'].get('--password'):
                    return result
            case 'buy'|'sell':
                if result['args'].get('--currency') and result['args'].get('--amount'):
                    return result
            case 'show-portfolio':
                return result
            case 'exit':
                exit()
            case 'get-rate':
                valuta_from = result['args'].get('--from')
                valuta_to   = result['args'].get('--to')
                if valuta_from in VALUTAS and valuta_to in VALUTAS:
                    return result
                
        return {'cmd':'unknow'}


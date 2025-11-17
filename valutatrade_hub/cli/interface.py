from dataclasses import dataclass
from .parser import ParserCLI 
import readline
from valutatrade_hub.core.consts import VALUTAS
from valutatrade_hub.core.exceptoins import CurrencyNotFoundError

def enable_arrow_keys():
    ...
def set_history_length():
    readline.set_history_length(100)


@dataclass
class CLI:
    parser = ParserCLI()
    prompt: str = '>>>'
    def input(self) -> dict:
        try:
            return self.processing(input(self.prompt))
        except KeyboardInterrupt as e:
            return {'cmd':'unknow', 'exception': e}

    def processing(self, user_input):
        result = self.parser.run(user_input)
        match result['cmd']:
            case 'register'|'login'|'change-password':
                if result['cmd'] == 'change-password' and result['args'].get('--password'):
                    return result
                if result['args'].get('--username') and result['args'].get('--password'):
                    return result
            case 'buy'|'sell':
                currency = result['args'].get('--currency')
                if currency and result['args'].get('--amount'):
                    for aliases in VALUTAS.keys():
                        if currency in aliases:
                            result['args']['--currency'] = VALUTAS[aliases]
                            return result
                    else:
                        raise CurrencyNotFoundError                            
                return {'cmd':'unknow'}
            case 'show-portfolio':
                return result
            case 'exit':
                return result
            case 'get-rate':
                valuta_from = result['args'].get('--from')
                valuta_to   = result['args'].get('--to')
                for aliases in VALUTAS.keys():
                    if valuta_from in aliases:
                        result['args']['--from'] = VALUTAS[aliases]
                        break
                else:
                    raise CurrencyNotFoundError  
                       
                for aliases in VALUTAS.keys():
                    if valuta_to in aliases:
                        result['args']['--to'] = VALUTAS[aliases]
                        return result
                raise CurrencyNotFoundError
                
        return {'cmd':'unknow'}


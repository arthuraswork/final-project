import readline
from dataclasses import dataclass

from valutatrade_hub.core.exceptoins import CurrencyNotFoundError
from valutatrade_hub.infra.consts import HELP_COMMANDS, VALUTAS
from valutatrade_hub.infra.logger import log

from .parser import ParserCLI


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
                if (result['cmd'] == 'change-password' 
                    and result['args'].get('--password')):
                    return result
                if (result['args'].get('--username') 
                    and 
                    result['args'].get('--password')):
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
            
            case 'help':
                log.show(';\n'.join(HELP_COMMANDS))
                return result
            
            case 'update-rates':
                return result

            case 'get-rate'|'show-rate':
                valuta_from = result['args'].get('--from')
                valuta_to   = result['args'].get('--to')
                if not valuta_from and not valuta_to and result['cmd'] == 'show-rate':
                    return result

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


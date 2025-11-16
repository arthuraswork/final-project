from valutatrade_hub.core.consts import TokenArgs, TokenCmdType
from valutatrade_hub.core.decorators import handler_logger
  
class ParserCLI:
    @handler_logger
    def run(self, input: str):
        try:
            return self.parse(input)
        except Exception as e:
            return {'cmd':'exception', 'exception': e}

    def parse(self, input: str):
        tokenized = input.split()
        args: dict = {}
        command_type: str = tokenized[0] if tokenized[0] in [e.value for e in list(TokenCmdType)] else 'unknown'
        if command_type in ['exit']:
            return {'cmd':command_type}
        for i, token in enumerate(tokenized):
            if token in [e.value for e in list(TokenArgs)]:
                args[token] = tokenized[i+1]
        return {'cmd':command_type, 'args':args}
from dataclasses import dataclass
from consts import TokenArgs, TokenCmdType

def handler_logger(func):
    def wrapper(*args,**kwargs):
        result =  func(*args,**kwargs)
        if result:
          print(f'command: {result.get('cmd')}')
        return result 
    return wrapper
  
@dataclass
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
      for i, token in enumerate(tokenized):
          if token in [e.value for e in list(TokenArgs)]:
            args[token] = tokenized[i+1]
      return {'cmd':command_type, 'args':args}
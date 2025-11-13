from dataclasses import dataclass
from enum import Enum 

class TokenCmdType(Enum):
    REGISTER = "register"
    LOGIN    = "login"
    BUY      = "buy"
    
    
class TokenArgs(Enum):
    USERNAME = '--username'
    PASSWORD = '--password'
    CURRENCY = '--currency'
    AMOUNT   = '--amount'
    SELL = "sell"
    BALANCE = "balance"
    PORTFOLIO = "portfolio"
    LOGOUT = "logout"
    EXIT = "exit"


@dataclass
class ParserCLI:
    
    def run(self, input: str):
      try:
        return self.parse(input)
      except Exception as e:
        return {'cmd':'exception', 'exception': e}
    

    def parse(self, input: str):
      tokenized = input.split()
      args: dict = {
          
      }
      command_type: str = tokenized[0] if tokenized[0] in [e.value for e in list(TokenCmdType)] else 'unknown'
      for i, token in enumerate(tokenized):
          if token in [e.value for e in list(TokenArgs)]:
            args[token] = tokenized[i+1]
      return {'cmd':command_type, 'args':args}
        
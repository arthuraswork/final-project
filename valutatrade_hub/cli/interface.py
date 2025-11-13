from dataclasses import dataclass
from parser import ParserCLI 
@dataclass
class CLI:
    parser = ParserCLI()
    def input(self,input):
        result = self.parser.run(input)
        print(result)

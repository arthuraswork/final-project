from valutatrade_hub.core.usercases import UserCase
from dataclasses import dataclass
from valutatrade_hub.parser_service.updater import RatesUpdater

@dataclass
class Program:
    user_case = UserCase()
    updater = RatesUpdater() 
    def event_loop(self):
        while True:
        
            result = self.user_case.user_request()
            if result == 'update-rates':
                self.updater.update()        
            
def main():
    Program().event_loop()
    
if __name__ == '__main__':
    main()
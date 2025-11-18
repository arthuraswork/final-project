from valutatrade_hub.core.usercases import UserCase
from dataclasses import dataclass
from valutatrade_hub.parser_service.updater import RatesUpdater
from valutatrade_hub.parser_service.scheduler import Scheduler
@dataclass
class Program:
    user_case = UserCase()
    updater = RatesUpdater() 
    scheduler = Scheduler()

    def event_loop(self):
        self.updater.update()  
        while True:

            if self.scheduler.time_check():
                self.updater.update()

            result = self.user_case.user_request()
            if result == 'update-rates':
                self.updater.update()  
            
            elif result == 'exit':
                print('Bye bye')      
                break
def main():
    Program().event_loop()
    
if __name__ == '__main__':
    main()
from valutatrade_hub.core.usercases import UserCase
from dataclasses import dataclass

@dataclass
class Program:
    user_case = UserCase() 
    def event_loop(self):
        while True:
            self.user_case.user_request()
            
def main():
    Program().event_loop()
    
if __name__ == '__main__':
    main()
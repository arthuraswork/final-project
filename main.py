from valutatrade_hub.core.usercases import UserCase
from dataclasses import dataclass

@dataclass
class Menu:
    user_case = UserCase() 
    def event_loop(self):
        while True:
            self.user_case.user_request()
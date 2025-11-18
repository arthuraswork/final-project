from dataclasses import dataclass
from datetime import datetime

from .consts import DATE_FORMAT


@dataclass
class Logger:
    alert_color = '\033[91m'
    clean = '\033[0m'


    def get_current_time(self):
        return datetime.now().strftime(DATE_FORMAT)

    def alert(self,msg):
        print(f"{self.alert_color}[!!!!]{self.clean} {msg}: {self.get_current_time()}")

    def info(self, msg):
        print(f"[info] {msg}: {self.get_current_time()}")
    def show(self,msg):
        print(msg)
log = Logger()
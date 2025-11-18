from datetime import datetime

from valutatrade_hub.infra.logger import log

from .config import ParserConfig


class Scheduler:
    """
    планнировщих обновлений курсов - 
    проверяет каждый цикл если
    время прошло - абдейт
    """
    def __init__(self):
        self.init_time = datetime.now()
        self.config = ParserConfig()
        self.timeout_seconds = self.config.REQUEST_TIMEOUT * 60
    def time_check(self):
        now = datetime.now()
        difference = (now - self.init_time).total_seconds()
        if difference > self.timeout_seconds:
            self.init_time = now
            log.info('Planned database updating')
            return True
        return False
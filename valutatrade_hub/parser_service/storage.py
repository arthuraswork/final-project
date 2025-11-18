from dataclasses import dataclass

from valutatrade_hub.core.utils import RatesHistoryDB


@dataclass
class HistoryManager:
    """
    менеджер работы с историей курсов))
    """
    history = RatesHistoryDB()
      
from dataclasses import dataclass

from valutatrade_hub.core.utils import RatesHistoryDB


@dataclass
class HistoryManager:
    history = RatesHistoryDB()
      
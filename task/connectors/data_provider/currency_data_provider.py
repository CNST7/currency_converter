from abc import ABC, abstractmethod

from dataclasses import dataclass
from datetime import date as date_


@dataclass(frozen=True)
class CurrencyRate:
    date: date_
    rate: float


class CurrencyDataProvider(ABC):
    @abstractmethod
    def get_data(self, currency: str) -> list[CurrencyRate]:
        raise NotImplementedError()

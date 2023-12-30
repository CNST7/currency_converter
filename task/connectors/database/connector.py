from typing import Protocol
from task.currency_converter import ConvertedPricePLN
from task.domain import models as domain_models


class DatabaseConnector(Protocol):
    def save(self, entity: ConvertedPricePLN) -> int:
        ...

    def get_all(self) -> list[domain_models.ConvertedPricePLN]:
        ...

    def get_by_id(self, id: int) -> domain_models.ConvertedPricePLN | None:
        ...
